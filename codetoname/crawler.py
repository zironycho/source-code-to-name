# -*- coding: utf-8 -*-
import json
import github
import elasticsearch
import elasticsearch_dsl
import logging

from elasticsearch_dsl.aggs import A
from codetoname.features import from_repo

logger = logging.getLogger(__package__)
handler = logging.FileHandler('crawler.log')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Crawler:
    def __init__(self, index='codetoname', page_num=0, page_size=10,
                 language='python', account=None, password=None):
        self._es = elasticsearch.Elasticsearch()
        self._es_index = index
        self._page_num = page_num
        self._page_size = page_size
        self._language = language
        if account and password:
            github_client = github.Github(account, password)
            print('Hi, {}'.format(github_client.get_user().name))
        else:
            github_client = github.Github()

        self._github_response = github_client.search_repositories(
            query='language:{}'.format(self._language.strip()))

        self._latest_repo_index = False

    def delete_index(self):
        if self._es.indices.exists(index=self._es_index):
            self._es.indices.delete(index=self._es_index)

    def create_index(self):
        if not self._es.indices.exists(index=self._es_index):
            self._es.indices.create(index=self._es_index)

    def fetch_github_repos(self, page_size=None):
        # update page size
        if page_size:
            self._page_size = page_size

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
        repos = self._github_response[start_index:end_index]
        return [{'url': r.clone_url, 'branch': r.default_branch, 'github_id': r.id, 'fork': r.fork} for r in repos]

    def next(self):
        self.create_index()
        for repo in self.fetch_github_repos():
            logger.info('[{:4d}] {}'.format(self._page_num, repo['url']))
            if not self.exists_repos_in_database(repo['github_id']):
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
                    logger.error(repo)
                    logger.error(f) if f else None
                    logger.error(e)

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
