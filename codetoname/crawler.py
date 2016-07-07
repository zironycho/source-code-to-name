# -*- coding: utf-8 -*-
import json

import elasticsearch
import elasticsearch_dsl
import github

from codetoname.features import from_repo


def fetch_github_repos(language, repo_size=10, repo_page=0):
    start_offset = repo_size * repo_page
    end_offset = start_offset + repo_size
    repos = github.Github().search_repositories(query='language:{}'.format(language.strip()))
    repos = repos[start_offset:end_offset]
    return [{'url': r.clone_url, 'branch': r.default_branch, 'github_id': r.id, 'fork': r.fork} for r in repos]


class Crawler:
    def __init__(self, page_num=0, page_size=10):
        self.es = elasticsearch.Elasticsearch()
        self.es_index = 'codetoname'
        self.page_num = page_num
        self.page_size = page_size

        if not self.es.indices.exists(index=self.es_index):
            self.es.indices.create(index=self.es_index)

    def next(self):
        language = 'python'
        for repo in fetch_github_repos(language=language, repo_size=self.page_size, repo_page=self.page_num):
            if 0 != elasticsearch_dsl\
                    .Search(using=self.es, index=self.es_index, doc_type=language)\
                    .query('term', github_id=repo['github_id'])\
                    .count():
                continue

            try:
                features = from_repo(repo, language=language)
                for f in features:
                    self.es.index(
                        index=self.es_index,
                        doc_type=language,
                        body={'repo': repo, 'feature': json.dumps(f)}
                    )
                if not features:
                    self.es.index(
                        index=self.es_index,
                        doc_type=language,
                        body={'repo': repo})
                self.es.indices.refresh(index=self.es_index)
            except Exception as e:
                print(repo)
                print(f) if f else None
                print(e)

        self.page_num += 1
