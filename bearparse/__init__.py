import re
from os import sep
from sys import argv
from typing import Any, Callable, List, Optional, Type, Union

import attr
from attr.validators import instance_of

__version__ = "0.1.1"


@attr.s(slots=True)
class Argument:
    r"""An argument to be parsed.

    :param name: Name of the argument, must match `^[\w]\{1,}$`
    :param description: Argument description
    :param required: If the argument is required
    :param value: Value of the argument
    :param type: Type of the argument
    :param parser: Custom parser function
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


@attr.s()
class ArgumentParser:
    r"""Custom ArgumentParser for non-standard argument passing.

    :param description: Program description
    :param arguments: Arguments to be parsed
    :param format: Custom argument format, default `^([\w]{1,})=(.*)$`
    :param help: If help string should be generated
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

    def add_argument(self, arg: Union[Argument, dict]) -> None:
        """Add an argument to be parsed.

        :param arg: Argument/dict to parse
        """
        if isinstance(arg, dict):
            arg = Argument(**arg)
        self.arguments.append(arg)
        self._arg_lookup[arg.name] = arg

    def parse_args(self, args: Optional[list] = None) -> dict:
        parsed = {}
        if not args:
            args = argv[1:]
        print(args)
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
            self.__setattr__(arg.name, arg.value)
            if arg.name not in parsed:
                if arg.required:
                    raise ValueError(f"Missing required argument: {arg.name}")
                parsed[arg.name] = arg.value
        self._parsed = parsed
