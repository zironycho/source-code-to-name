# -*- coding: utf-8 -*-
import os

__languages = {
	'python': '.py'
}


def support_languages():
	return __languages.keys()


def language_to_extension(language):
	return __languages[language]


def path_to_language(path):
	ext = os.path.splitext(path)[1]
	for k, v in __languages.items():
		if v == ext:
			return k
	return False
