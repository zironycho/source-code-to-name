# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestApi(unittest.TestCase):
    def test_getname_with_empty_code(self):
        self.assertFalse(codetoname.getname('', ''))

    def test_getname(self):
        with open('./test/samples/get_a.txt', 'rt') as f:
            code_block = f.read()
            self.assertEqual('get_a', codetoname.getname(code_block, 'python'))
