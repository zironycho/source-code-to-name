# -*- coding: utf-8 -*-
import tempfile
import github
import git
import os
import shutil

from codetoname.features import extract_feature
from codetoname.features.language import language_to_extension


def fromgithub(query, language, repo_size=10):
	ext = language_to_extension(language)
	tempdirs = []
	try:
		features = []
		repos = github.Github().search_repositories(query=query)[0:repo_size]
		for repo in repos:
			tempdir = tempfile.mkdtemp(prefix=__name__)
			tempdirs.append(tempdir)
			print('temp dir: {}'.format(tempdir))
			git.Repo.clone_from(url=repo.clone_url, to_path=tempdir, branch=repo.default_branch)
			for r, d, fs in os.walk(tempdir):
				for f in fs:
					if f.endswith(ext):
						features += fromfile(os.path.join(r, f))
	finally:
		for tempdir in tempdirs:
			shutil.rmtree(tempdir, ignore_errors=True)

	return features, [r.clone_url for r in repos]


def fromfile(filename):
	return extract_feature(filename)
