import elasticsearch
import elasticsearch_dsl as es_dsl
import json

import codetoname
from config import ES_CONFIG


def main():
    es = elasticsearch.Elasticsearch()
    language = 'python'

    if not es.indices.exists(index=ES_CONFIG['index']):
        es.indices.create(index=ES_CONFIG['index'])

    for page in range(0, 10):
        for repo in codetoname.crawler.fetch_github_repos(language='python', repo_size=100, repo_page=page):
            q = es_dsl.Search(using=es, index=ES_CONFIG['index'], doc_type=language) \
                .query('term', github_id=repo['github_id'])

            # already inserted
            if 0 != q.count():
                continue

            try:
                features, num = codetoname.crawler.from_gitrepo([repo], language=language)

                for f in features:
                    es.index(index=ES_CONFIG['index'], doc_type=language, body={'repo': repo, 'feature': json.dumps(f)})
                if not features:
                    es.index(index=ES_CONFIG['index'], doc_type=language, body={'repo': repo})
                es.indices.refresh(index=ES_CONFIG['index'])
            except Exception as e:
                print(f) if f else None
                print(repo)
                print(e)


if __name__ == '__main__':
    main()
