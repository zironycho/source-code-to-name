# -*- coding: utf-8 -*-
import tempfile
import github
import git
import os
import shutil

from codetoname.features import extract_feature
from codetoname.features.language import language_to_extension


def fetch_github_repos(language, repo_size=10, repo_page=0):
    start_offset = repo_size * repo_page
    end_offset = start_offset + repo_size
    repos = github.Github().search_repositories(query='language:{}'.format(language.strip()))
    repos = repos[start_offset:end_offset]
    return [{'url': r.clone_url, 'branch': r.default_branch, 'id': r.id} for r in repos]


def from_gitrepo(gitrepo, language):
    paths = []
    features = []
    ext = language_to_extension(language)
    try:
        for repo in gitrepo:
            if ('url' not in repo) or not repo['url']:
                continue

            kwargs = {}
            if 'branch' in repo:
                kwargs['branch'] = repo['branch']

            paths.append(tempfile.mkdtemp(prefix=__name__))
            print('temp dir: {}'.format(paths[-1]))
            git.Repo.clone_from(url=repo['url'], to_path=paths[-1], **kwargs)
            for r, d, fs in os.walk(paths[-1]):
                for f in fs:
                    if f.endswith(ext):
                        features += from_file(os.path.join(r, f))
    finally:
        for path in paths:
            shutil.rmtree(path, ignore_errors=True)

    return features, len(paths)


def from_file(filename):
    return extract_feature(filename)
