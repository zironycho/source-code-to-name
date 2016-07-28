# -*- coding: utf-8 -*-
import json
import github
import elasticsearch
import elasticsearch_dsl

from datetime import datetime
from elasticsearch_dsl.aggs import A
from .features import from_repo
from .log import get_logger


class Crawler:
    def __init__(self, index='codetoname', page_num=0, page_size=30,
                 language='python', account=None, password=None):
        self._es = elasticsearch.Elasticsearch()
        self._es_index = index
        self._page_num = page_num
        self._page_size = page_size
        self._language = language
        self._total_page_num = 0
        if account and password:
            github_client = github.Github(account, password, per_page=page_size)
            print('Hi, {}'.format(github_client.get_user().name))
        else:
            github_client = github.Github(per_page=page_size)

        self._github_client = github_client
        self._github_response = None
        self._latest_repo_updated = None
        self._latest_repo_index = False
        self._update_searching_response()

    def delete_index(self):
        if self._es.indices.exists(index=self._es_index):
            self._es.indices.delete(index=self._es_index)

    def create_index(self):
        if not self._es.indices.exists(index=self._es_index):
            self._es.indices.create(index=self._es_index)

    def _update_searching_response(self):
        if not self._latest_repo_updated:
            self._latest_repo_updated = datetime.utcnow()

        date = self._latest_repo_updated.isoformat().split('.')[0]
        query = 'fork:false language:{} pushed:<={}'.format(
            self._language.strip(), date)

        # language:python fork:false updated:<=2016-07-28T13:37:01.262955
        self._github_response = self._github_client.search_repositories(
            query=query,
            sort='updated',
            order='desc')

    def fetch_github_repos(self):
        # calculate new start-end indices
        if self._latest_repo_index:
            start_index = self._latest_repo_index
        else:
            start_index = self._page_size * self._page_num
        end_index = start_index + self._page_size

        # update latest index, and page num
        self._latest_repo_index = end_index
        self._page_num += 1

        # fetch
        repos = list(self._github_response[start_index:end_index])
        if not repos:
            self._page_num = 0
            self._latest_repo_index = 0
            self._update_searching_response()

            start_index = 0
            end_index = self._page_size
            repos = list(self._github_response[start_index:end_index])

        ret = []
        for r in repos:
            self._latest_repo_updated = min(self._latest_repo_updated, r.updated_at)
            ret.append({'url': r.clone_url, 'branch': r.default_branch, 'github_id': r.id, 'fork': r.fork})
        return ret

    def next(self):
        self.create_index()
        self._total_page_num += 1
        log = get_logger()
        for repo in self.fetch_github_repos():
            log.info('[{:4d}] {}'.format(self._total_page_num, repo['url']))
            if not self.exists_repos_in_database(repo['github_id']):
                f = None  # don't remove this line, it is used for exception handling
                try:
                    features = from_repo(repo, language=self._language)
                    for f in features:
                        self._es.index(
                            index=self._es_index,
                            doc_type=self._language,
                            body={'repo': repo, 'feature': json.dumps(f)}
                        )
                    if not features:
                        self._es.index(
                            index=self._es_index,
                            doc_type=self._language,
                            body={'repo': repo})
                    self._es.indices.refresh(index=self._es_index)
                except Exception as e:
                    log.error(repo)
                    log.error(e)
                    log.error(f) if f else None

    def exists_repos_in_database(self, github_id):
        if 0 != elasticsearch_dsl \
                .Search(using=self._es, index=self._es_index, doc_type=self._language) \
                .query('term', repo__github_id=github_id) \
                .count():
            return True
        return False

    def num_features(self):
        return self._es.count(index=self._es_index)['count']

    def num_repos(self):
        if self._es.indices.exists(index=self._es_index):
            s = elasticsearch_dsl.Search(using=self._es, index=self._es_index, doc_type=self._language)
            s.aggs.bucket('num_repos', A('cardinality', field='repo.github_id'))
            response = s.execute()
            return response.aggregations.num_repos.value
        return 0

    def get_features(self):
        if self._es.indices.exists(index=self._es_index):
            s = elasticsearch_dsl.Search(using=self._es, index=self._es_index, doc_type=self._language)
            response = s.execute()
            if 0 != len(response.hits):
                return response.hits
        return False
