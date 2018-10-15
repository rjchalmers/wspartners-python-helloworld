import unittest

import helloworld.server as testmod


class TestStatus(unittest.TestCase):

    def test_returns_ok(self):
        response = testmod.status()
        self.assertEqual(response, "OK")
