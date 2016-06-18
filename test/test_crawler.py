# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestCrawler(unittest.TestCase):
	def test_from_github_one_repo(self):
		features, urls = codetoname.crawler.fromgithub('python', 'python', repo_size=1)
		self.assertTrue(features)
		self.assertEqual(1, len(urls))

	def test_from_github_multiple_repo(self):
		features, urls = codetoname.crawler.fromgithub('python', 'python', repo_size=2)
		self.assertTrue(features)
		self.assertEqual(2, len(urls))

	def test_from_github_unsupported(self):
		self.assertRaises(KeyError, codetoname.crawler.fromgithub, 'python', 'c++')

	def test_from_file(self):
		features = codetoname.crawler.fromfile('./test/samples/one_function.py')
		self.assertTrue(features)
