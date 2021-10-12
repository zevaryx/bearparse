import json
import os
import unittest

import toml
import yaml

try:
    from yaml import CDumper as Dumper, CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

from bearparse import Argument, ArgumentParser, FileType
from bearparse.parsers import bool_parser


class TestArgparse(unittest.TestCase):

    # Test ArgumentParser
    def test_basic(self):
        """Test basic functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument"))
        a.add_argument({"name": "test2", "description": "Test Argument 2"})

        self.assertIsNone(a.parsed)

        parsed = a.parse_args(["test=test"])
        self.assertEqual("test", parsed.test)
        self.assertIsNone(parsed.test2)
        self.assertEqual({"test": "test", "test2": None}, a.parsed)
        self.assertEqual(
            "UnitTest\nUsage: __main__.py test=<value> test2=<value>"
            "\n        test  :  Test Argument\n       test2  :  Test Argument 2\n",
            a.help_message,
        )

    def test_no_help(self):
        """Test help=False"""
        a = ArgumentParser(description="UnitTest", help=False)
        a.add_argument(Argument(name="test", description="Test Argument", required=True))

        self.assertIsNone(a.help_message)

    def test_required(self):
        """Test required arguments"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument", required=True))

        self.assertRaises(ValueError, a.parse_args)

    def test_argv(self):
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument"))

        parsed = a.parse_args()
        self.assertIsNone(parsed.test)
        self.assertEqual({"test": None}, a.parsed)

    def test_custom_format(self):
        a = ArgumentParser(description="UnitTest", format=r"^([\w]{1,})-(.*)$")
        a.add_argument(Argument(name="test", description="Test Argument"))

        parsed = a.parse_args(["test-test"])
        self.assertEqual("test", parsed.test)
        self.assertEqual({"test": "test"}, a.parsed)

    # Test Argument
    def test_argument_parser(self):
        """Test argument parser functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument", parser=bool_parser))

        for test in ["True", "true", "Yes", "yes", "T", "t", "Y", "y", True, 1]:
            parsed = a.parse_args([f"test={test}"])
            self.assertEqual(True, parsed.test)
            self.assertEqual({"test": True}, a.parsed)

    def test_type_conversion(self):
        """Test argument conversion functionality"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument", type=bool, parser=bool_parser))
        a.add_argument(Argument(name="test2", description="Test Argument 2", type=int))
        a.add_argument(Argument(name="test3", description="Test Argument 3", type=float))
        parsed = a.parse_args(["test=True", "test2=31", "test3=3.1"])

        self.assertEqual(True, parsed.test)
        self.assertEqual(31, parsed.test2)
        self.assertEqual(3.1, parsed.test3)
        self.assertEqual({"test": True, "test2": 31, "test3": 3.1}, a.parsed)

    def test_argument_name(self):
        """Test argument name checking"""
        self.assertRaises(ValueError, Argument, name="bad name")
        self.assertRaises(ValueError, Argument, name="bad-name")

    def test_to_dict(self):
        """Test ArgumentParser to_dict"""
        a = ArgumentParser(description="UnitTest")
        a.add_argument(Argument(name="test", description="Test Argument"))
        a_dict = {
            "description": "UnitTest",
            "format": r"^([\w]{1,})=(.*)$",
            "help": True,
            "arguments": [{"name": "test", "description": "Test Argument", "required": False, "type": None}],
        }

        self.assertEqual(a.to_dict(), a_dict)

    def test_from_dict(self):
        """Test creating argparser from dict"""
        data = {"description": "UnitTest", "arguments": [{"name": "test", "description": "Test Argument"}]}
        _ = ArgumentParser.from_dict(data)

    def test_from_file(self):
        """Test creating argparser from file"""
        data = {"description": "UnitTest", "arguments": [{"name": "test", "description": "Test Argument"}]}
        with open("tmp.json", "w+") as f:
            json.dump(data, f)
        _ = ArgumentParser.from_file("tmp.json", FileType.JSON)
        os.unlink("tmp.json")
        with open("tmp.yaml", "w+") as f:
            yaml.dump(data, f, Dumper=Dumper)
        _ = ArgumentParser.from_file("tmp.yaml", FileType.YAML)
        os.unlink("tmp.yaml")
        with open("tmp.toml", "w+") as f:
            toml.dump(data, f)
        _ = ArgumentParser.from_file("tmp.toml", FileType.TOML)
        self.assertRaises(ValueError, ArgumentParser.from_file, "tmp.toml", 4)
        os.unlink("tmp.toml")
