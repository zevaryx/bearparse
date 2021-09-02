import unittest

from bearparse import Argument, ArgumentParser
from bearparse.parsers import bool_parser


class TestArgparse(unittest.TestCase):

    # Test ArgumentParser
    def test_basic(self):
        """Test basic functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument"))
        a.add_argument({"name": "test2", "description": "Test Argument 2"})

        self.assertIsNone(a.parsed)

        a.parse_args(["test=test"])
        self.assertEqual("test", a.test)
        self.assertIsNone(a.test2)
        self.assertEqual({"test": "test", "test2": None}, a.parsed)
        self.assertEqual(
            "UnitTest\nUsage: __main__.py test=<value> test2=<value>"
            "\n        test  :  Test Argument\n       test2  :  Test Argument 2\n",
            a.help_message,
        )

    def test_argv(self):
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument"))

        a.parse_args()
        self.assertIsNone(a.test)
        self.assertEqual({"test": None}, a.parsed)

    def test_custom_format(self):
        a = ArgumentParser(description="UnitTest", format=r"^([\w]{1,})-(.*)$")
        a.add_argument(Argument(name="test", description="Test Argument"))

        a.parse_args(["test-test"])
        self.assertEqual("test", a.test)
        self.assertEqual({"test": "test"}, a.parsed)

    # Test Argument
    def test_argument_parser(self):
        """Test argument parser functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument", parser=bool_parser))

        for test in ["True", "true", "Yes", "yes", "T", "t", "Y", "y", True, 1]:
            a.parse_args([f"test={test}"])
            self.assertEqual(True, a.test)
            self.assertEqual({"test": True}, a.parsed)

    def test_type_conversion(self):
        """Test argument conversion functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument", type=bool, parser=bool_parser))
        a.add_argument(Argument(name="test2", description="Test Argument 2", type=int))
        a.add_argument(Argument(name="test3", description="Test Argument 3", type=float))
        a.parse_args(["test=True", "test2=31", "test3=3.1"])
        self.assertEqual(True, a.test)
        self.assertEqual(31, a.test2)
        self.assertEqual(3.1, a.test3)
        self.assertEqual({"test": True, "test2": 31, "test3": 3.1}, a.parsed)

    def test_argument_name(self):
        """Test argument name checking"""
        self.assertRaises(ValueError, Argument, name="bad name")
        self.assertRaises(ValueError, Argument, name="bad-name")
