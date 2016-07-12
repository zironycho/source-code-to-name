# -*- coding: utf-8 -*-
import json

import elasticsearch
import elasticsearch_dsl
import github
from elasticsearch_dsl.aggs import A

from codetoname.features import from_repo


def fetch_github_repos(language, repo_size=10, repo_page=0, account=None, password=None):
    start_offset = repo_size * repo_page
    end_offset = start_offset + repo_size

    if account and password:
        github_client = github.Github(account, password)
    else:
        github_client = github.Github()
    repos = github_client.search_repositories(query='language:{}'.format(language.strip()))
    repos = repos[start_offset:end_offset]
    return [{'url': r.clone_url, 'branch': r.default_branch, 'github_id': r.id, 'fork': r.fork} for r in repos]


class Crawler:
    def __init__(self, index='codetoname', page_num=0, page_size=10, account=None, password=None):
        self._es = elasticsearch.Elasticsearch()
        self._es_index = index
        self._page_num = page_num
        self._page_size = page_size
        self._account = account
        self._password = password

    def delete_index(self):
        if self._es.indices.exists(index=self._es_index):
            self._es.indices.delete(index=self._es_index)

    def create_index(self):
        if not self._es.indices.exists(index=self._es_index):
            self._es.indices.create(index=self._es_index)

    def next(self):
        self.create_index()
        language = 'python'
        repos = fetch_github_repos(language=language,
                                   repo_size=self._page_size, repo_page=self._page_num,
                                   account=self._account, password=self._password)
        for repo in repos:
            if 0 != elasticsearch_dsl\
                    .Search(using=self._es, index=self._es_index, doc_type=language)\
                    .query('term', github_id=repo['github_id'])\
                    .count():
                continue

            try:
                features = from_repo(repo, language=language)
                for f in features:
                    self._es.index(
                        index=self._es_index,
                        doc_type=language,
                        body={'repo': repo, 'feature': json.dumps(f)}
                    )
                if not features:
                    self._es.index(
                        index=self._es_index,
                        doc_type=language,
                        body={'repo': repo})
                self._es.indices.refresh(index=self._es_index)
            except Exception as e:
                print(repo)
                print(f) if f else None
                print(e)

        self._page_num += 1

    def num_features(self):
        return self._es.count(index=self._es_index)['count']

    def num_repos(self, language):
        if self._es.indices.exists(index=self._es_index):
            s = elasticsearch_dsl.Search(using=self._es, index=self._es_index, doc_type=language)
            s.aggs.bucket('num_repos', A('cardinality', field='repo.github_id'))
            response = s.execute()
            return response.aggregations.num_repos.value
        return 0
