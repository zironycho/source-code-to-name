# -*- coding: utf-8 -*-
import unittest
import codetoname


class TestApi(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_getname_with_empty_code(self):
        self.assertFalse(codetoname.getname('', ''))

    def test_getname(self):

        code_block =\
            """
def unknown_name():
    return a
            """
        self.assertEqual('get_a', codetoname.getname(code_block, 'python'))
