# -*- coding: utf-8 -*-
import unittest

import codetoname

print(__name__)


class TestCrawler(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_from_github(self):
		features = codetoname.crawler.fromgithub('python', 'python')
		self.assertTrue(features)

	def test_from_github_unsupported(self):
		self.assertRaises(KeyError, codetoname.crawler.fromgithub, 'python', 'c++')

	def test_from_file(self):
		features = codetoname.crawler.fromfile('./test/samples/one_function.py')
		self.assertTrue(features)
