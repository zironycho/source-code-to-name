import os
import unittest

from codetoname import get_logger
from codetoname.log import _logger_filename


class TestLogger(unittest.TestCase):
    def tearDown(self):
        os.remove(_logger_filename)

    def test_many_calling(self):
        for i in range(100000):
            get_logger().error('log {}'.format(i))
        self.assertTrue(True)
