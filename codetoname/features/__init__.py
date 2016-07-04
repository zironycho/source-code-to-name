# -*- coding: utf-8 -*-
from codetoname.features.language import path_to_language, support_languages
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
