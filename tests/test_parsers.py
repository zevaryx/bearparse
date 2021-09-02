import unittest

from bearparse import parsers


class TestArgparse(unittest.TestCase):
    def test_bool_parser(self):
        """Test bool_parser"""
        tests = ["True", "true", "Yes", "yes", "T", "t", "Y", "y", True, 1]
        for test in tests:
            self.assertTrue(parsers.bool_parser(test))
        tests = ["False", "false", "No", "no", "F", "f", "N", "n", False, 0]
        for test in tests:
            self.assertFalse(parsers.bool_parser(test))

    def test_float_parser(self):
        """Test float_parser"""
        self.assertEqual(4, parsers.float_parser("4"))
        self.assertEqual(4.1, parsers.float_parser("4.1"))
        self.assertEqual(0, parsers.float_parser("0"))
        self.assertIsNone(parsers.float_parser("asdf"))
        self.assertIsNone(parsers.float_parser("True"))
        self.assertEqual(1, parsers.float_parser(True))
        self.assertEqual(0, parsers.float_parser(False))

    def test_int_parser(self):
        """Test int_parser"""
        self.assertEqual(4, parsers.int_parser("4"))
        self.assertEqual(4, parsers.int_parser("4.1"))
        self.assertEqual(0, parsers.int_parser("0"))
        self.assertIsNone(parsers.int_parser("asdf"))
        self.assertIsNone(parsers.int_parser("True"))
        self.assertEqual(1, parsers.int_parser(True))
        self.assertEqual(0, parsers.int_parser(False))
