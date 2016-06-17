# -*- coding: utf-8 -*-
import unittest

from codetoname import features


class TestFeature(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_feature_nofile(self):
		self.assertRaises(FileNotFoundError, features.extract_feature, '')

	def test_feature_nofunc(self):
		self.assertFalse(features.extract_feature('./test/samples/no_function.py'))

	def test_feature_onefunc(self):
		feat = features.extract_feature('./test/samples/one_function.py')
		self.assertTrue(feat)
		self.assertEqual('get_wsgi_application', feat[0]['name'])
		self.assertEqual(2, len(feat[0]['body']))
		self.assertEqual('Expr', feat[0]['body'][0])
		self.assertEqual('Return', feat[0]['body'][1])
