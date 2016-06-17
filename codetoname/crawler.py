# -*- coding: utf-8 -*-
import tempfile
import github
import git
import os
import shutil

from codetoname.features import extract_feature


__language_dict = {
	'python': '.py'
}


def fromgithub(query, language):
	ext = __language_dict[language]

	try:
		repo = github.Github().search_repositories(query=query)[0]

		tempdir = tempfile.mkdtemp(prefix=__name__)
		print(tempdir)
		git.Repo.clone_from(url=repo.clone_url, to_path=tempdir, branch=repo.default_branch)

		features = []
		for r, d, fs in os.walk(tempdir):
			for f in fs:
				if f.endswith(ext):
					features += fromfile(os.path.join(r, f))
	finally:
		shutil.rmtree(tempdir, ignore_errors=True)

	return features


def fromfile(filename):
	return extract_feature(filename)
