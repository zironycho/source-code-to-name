# -*- coding: utf-8 -*-
import unittest
from codetoname import features


class TestFeature(unittest.TestCase):
    def test_feature_no_file(self):
        self.assertRaises(Exception, features.extract_feature, '')

    def test_feature_no_func(self):
        self.assertFalse(features.extract_feature('./test/samples/no_function.py'))

    def test_feature_one_func(self):
        feat = features.extract_feature('./test/samples/one_function.py')
        self.assertTrue(feat)
        self.assertEqual('get_wsgi_application', feat[0]['name'])
        self.assertEqual(2, len(feat[0]['body']))
        self.assertEqual('Expr', feat[0]['body'][0])
        self.assertEqual('Return', feat[0]['body'][1])
