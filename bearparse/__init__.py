import json
import re
from enum import IntFlag
from os import sep
from pathlib import Path
from sys import argv
from typing import Any, Callable, List, Optional, Type, Union

import attr
import toml
import yaml
from attr.validators import instance_of

try:
    from yaml import CDumper as Dumper, CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

__version__ = "0.3.2"


class FileType(IntFlag):
    """FileType flag for reading/writing ArgumentParser files."""

    JSON = 1
    YAML = 2
    TOML = 3


@attr.s(slots=True)
class Argument:
    r"""An argument to be parsed.

    Attributes:
        name (str): Name of the argument, must match ``^[\w]\{1,}$``
        description (str): Argument description
        required (bool): If the argument is required, default ``False``
        value (Any): Value of the argument
        type (Type): Type of the argument
        parser (Callable): Custom parser function
    """
    name: str = attr.ib(validator=instance_of(str))
    description: Optional[str] = attr.ib(default=None, validator=instance_of(str))
    required: bool = attr.ib(default=False)
    value: Optional[Any] = attr.ib(default=None)
    type: Optional[Type] = attr.ib(default=None)
    parser: Optional[Callable[[Any], Any]] = attr.ib(default=None)

    @name.validator
    def _validate_name(self, attribute, value) -> None:
        if not re.fullmatch(r"^[\w]{1,}$", value):
            raise ValueError(r"Argument name must match the pattern '^[\w]\{1,}$'")

    def to_dict(self) -> dict:
        """Get the argument as a dict."""
        return {"name": self.name, "description": self.description, "required": self.required, "type": self.type}


class Args:
    """An object with parsed arguments"""

    def to_dict(self) -> dict:
        return self.__dict__

    def __getattr__(self, attr):
        return self.__dict__.get(attr, None)

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


@attr.s()
class ArgumentParser:
    r"""Custom ArgumentParser for non-standard argument passing.

    Attributes:
        description (str): Program description
        arguments (List[Argument]): Arguments to be parsed
        format (str): Custom argument format, default ``^([\w]{1,})=(.*)$``
        help (bool): If help string should be generated, default ``True``
    """
    description: Optional[str] = attr.ib(default=None)
    arguments: Optional[List[Argument]] = attr.ib(factory=list)
    format: str = attr.ib(default=r"^([\w]{1,})=(.*)$", validator=instance_of(str))
    help: bool = attr.ib(default=True)

    _arg_lookup: dict = attr.ib(factory=dict)
    _parsed: dict = attr.ib(factory=dict)

    @property
    def help_message(self) -> Optional[str]:
        """Auto-generated help message."""
        if not self.help:
            return None
        help_header = f"{self.description}\nUsage: {argv[0].split(sep)[-1]}"
        help_content = "\n"
        for arg in self.arguments:
            help_header += f" {arg.name}=<value>"
            help_content += f"{arg.name:>12}  :  {arg.description}\n"
        return help_header + help_content

    @property
    def parsed(self) -> Optional[dict]:
        """Return the parsed arguments as a dictionary."""
        if not self._parsed:
            return None
        return self._parsed

    def to_dict(self) -> dict:
        data = {"description": self.description, "format": self.format, "help": self.help, "arguments": []}
        for arg in self.arguments:
            data["arguments"].append(arg.to_dict())
        return data

    @classmethod
    def from_file(cls, path: Union[Path, str], filetype: FileType) -> "ArgumentParser":
        """Create an instance of ArgumentParser from a file.

        Args:
            path (Path | str): File path
            filetype (FileType): Type of file

        Returns:
            ArgumentParser: ArgumentParser created from file

        Raises:
            ValueError: An invalid FileType was passed in
        """
        if isinstance(path, str):
            path = Path(path)
        with path.open(encoding="utf8") as f:
            raw = f.read()
        if filetype == FileType.JSON:
            data = json.loads(raw)
        elif filetype == FileType.YAML:
            data = yaml.load(raw, Loader=Loader)
        elif filetype == FileType.TOML:
            data = toml.loads(raw)
        else:
            raise ValueError("Invalid filetype")

        return cls.from_dict(data)

    def to_file(self, path: Union[Path, str], filetype: FileType) -> None:
        """Save an instance of ArgumentParser to a file

        Args:
            path (Path | str): File path
            filetype (FileType): Type of file
        """
        if isinstance(path, str):
            path = Path(path)
        with path.open("w+", encoding="utf8") as f:
            data = self.to_dict()
            if filetype == FileType.JSON:
                data = json.dump(data, f, indent=4)
            elif filetype == FileType.YAML:
                data = yaml.dump(data, f, Dumper=Dumper)
            elif filetype == FileType.TOML:
                data = toml.dump(data, f)

    @classmethod
    def from_dict(cls, data: dict) -> "ArgumentParser":
        """Create an instance of ArgumentParser from a dict.

        Args:
            data (dict): Data dictionary
        """
        args = data.pop("arguments")
        parser = cls(**data)
        for arg in args:
            parser.add_argument(arg)

        return parser

    def add_argument(self, arg: Union[Argument, dict]) -> None:
        """Add an argument to be parsed.

        Args:
            arg (Argument | dict): Argument/dict to parse
        """
        if isinstance(arg, dict):
            arg = Argument(**arg)
        self.arguments.append(arg)
        self._arg_lookup[arg.name] = arg

    def parse_args(self, args: Optional[list] = None) -> Args:
        parsed = Args()
        if not args:
            args = argv[1:]
        for arg in args:
            match = re.match(self.format, arg)
            if match:
                name, value = match.groups()
                argument = self._arg_lookup.get(name)
                if argument:
                    if argument.parser is not None:
                        value = argument.parser(value)
                    if argument.type is not None:
                        value = argument.type(value)
                    argument.value = value
                parsed[name] = value
        for arg in self.arguments:
            if arg.name not in parsed.__dict__:
                if arg.required:
                    raise ValueError(f"Missing required argument: {arg.name}")
                parsed[arg.name] = None
        self._parsed = parsed.to_dict()

        return parsed
