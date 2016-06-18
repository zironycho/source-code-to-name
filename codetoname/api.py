# -*- coding: utf-8 -*-
from codetoname.features import extract_feature_from_code


def getname(code, language):
	if not code:
		return False

	feature = extract_feature_from_code(code, language)
	if not feature:
		return False

	return 'get_a'
