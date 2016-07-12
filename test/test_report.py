# -*- coding: utf-8 -*-
import json
import unittest

import elasticsearch
import codetoname


class TestReport(unittest.TestCase):
    def setUp(self):
        self.index = 'codetoname-dev'
        self.es = elasticsearch.Elasticsearch()
        if self.es.indices.exists(index=self.index):
            self.es.indices.delete(index=self.index)
        self.es.indices.create(index=self.index)

        self.es.index(index=self.index, doc_type='python', body={'feature': json.dumps({'name': 'hello'})})
        self.es.index(index=self.index, doc_type='python', body={'feature': json.dumps({'name': 'hello_my_function'})})
        self.es.index(index=self.index, doc_type='python', body={'feature': json.dumps({'name': 'not_hello'})})
        self.es.index(index=self.index, doc_type='python', body={'no': 'no...'})
        self.es.indices.refresh(index=self.index)

    def tearDown(self):
        self.es.indices.delete(index=self.index)

    def test_report_first_word(self):
        words = codetoname.report.first_words(index=self.index)
        self.assertIn('percentage', words[0])
        self.assertIn('word', words[0])
        self.assertEqual('hello', words[0]['word'])
        self.assertEqual(2/3.0*100, words[0]['percentage'])
        self.assertEqual('not', words[1]['word'])
        self.assertEqual(1/3.0*100, words[1]['percentage'])
