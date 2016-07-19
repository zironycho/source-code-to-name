import unittest

from codetoname.features.language import path_to_language


class TestLanguage(unittest.TestCase):
    def test_unsupported_language(self):
        path = '/recipe/.py'
        self.assertEqual('python', path_to_language(path))

        path = '/recipe/..py'
        self.assertFalse(path_to_language(path))
