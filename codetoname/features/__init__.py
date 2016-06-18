# -*- coding: utf-8 -*-
from codetoname.features.language import path_to_language
from . import python


def extract_feature(path):
	lang = path_to_language(path)
	if lang == 'python':
		return python.extract_feature(path)
	else:
		raise Exception('Unsupported language')
