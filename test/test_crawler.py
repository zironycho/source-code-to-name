# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestCrawler(unittest.TestCase):
    def test_from_gitrepo_one(self):
        features, num_processing = codetoname.crawler.from_gitrepo([], 'python')
        self.assertFalse(features)

    def test_from_gitrepo_one(self):
        gitrepo = [{'url': 'https://github.com/geekcomputers/Python.git'}]
        features, num_processing = codetoname.crawler.from_gitrepo(gitrepo, 'python')
        self.assertTrue(features)
        self.assertEqual(1, num_processing)

    def test_from_gitrepo_multiple(self):
        gitrepo = [{'url': 'https://github.com/geekcomputers/Python.git', 'branch': 'master'},
                   {'url': 'https://github.com/poise/python.git', 'branch': 'master'}]
        features, num_processing = codetoname.crawler.from_gitrepo(gitrepo, 'python')
        self.assertTrue(features)
        self.assertEqual(2, num_processing)

    def test_from_gitrepo_unsupported(self):
        self.assertRaises(KeyError, codetoname.crawler.from_gitrepo, [], 'c++')

    def test_fromfile(self):
        features = codetoname.crawler.from_file('./test/samples/one_function.py')
        self.assertTrue(features)

    def test_fetch_github_repos(self):
        repos = codetoname.crawler.fetch_github_repos('python', repo_page=0)
        self.assertEqual(10, len(repos))

        found = False
        for url in repos:
            if url['url'] == 'https://github.com/jkbrzt/httpie.git':
                found = True
        self.assertTrue(found)

        next_repos = codetoname.crawler.fetch_github_repos('python', repo_page=1, repo_size=15)

        the_same = True
        for u in next_repos:
            if u not in repos:
                the_same = False
        self.assertFalse(the_same)
