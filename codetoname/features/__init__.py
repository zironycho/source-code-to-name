# -*- coding: utf-8 -*-
import shutil
import tempfile

import os

import git

from codetoname.features.language import path_to_language, support_languages, language_to_extension
from . import python


def extract_feature(path):
    lang = path_to_language(path)
    if lang == 'python':
        return python.extract_feature(path)
    else:
        raise Exception('Unsupported language: {}'.format(path))


def extract_feature_from_code(code, language):
    if language == 'python':
        return python.extract_feature_from_code(code)
    else:
        raise Exception('Unsupported language')


def from_repo(repo, language):
    features = []
    ext = language_to_extension(language)
    path = tempfile.mkdtemp(prefix=__name__)
    try:
        if ('url' not in repo) or not repo['url']:
            pass
        else:
            kwargs = {}
            if 'branch' in repo:
                kwargs['branch'] = repo['branch']

            git.Repo.clone_from(url=repo['url'], to_path=path, **kwargs)
            for r, d, fs in os.walk(path):
                for f in fs:
                    if f.endswith(ext):
                        features += from_file(os.path.join(r, f))
    finally:
        shutil.rmtree(path, ignore_errors=True)
    return features


def from_file(filename):
    return extract_feature(filename)


