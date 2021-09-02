import re
from sys import argv
from typing import Any, Callable, List, Optional, Type, Union

import attr
from attr.validators import instance_of

__version__ = "0.0.1"


@attr.s(slots=True)
class Argument:
    name: str = attr.ib(validator=instance_of(str))
    description: Optional[str] = attr.ib(default=None, validator=instance_of(str))
    value: Optional[Any] = attr.ib(default=None)
    type: Optional[Type] = attr.ib(default=None)
    parser: Optional[Callable[[Any], Any]] = attr.ib(default=None)

    @name.validator
    def _validate_name(self, attribute, value):
        if not re.fullmatch(r"^[\w]{1,}$", value):
            raise ValueError(r"Argument name must match the pattern '^[\w]\{1,}$'")


@attr.s()
class ArgumentParser:
    description: Optional[str] = attr.ib(default=None)
    arguments: Optional[List[Argument]] = attr.ib(factory=list)
    format: str = attr.ib(default=r"^([\w]{1,})=(.*)$", validator=instance_of(str))
    help: bool = attr.ib(default=True)

    _arg_lookup: dict = attr.ib(factory=dict)
    _parsed: dict = attr.ib(factory=dict)

    @property
    def help_message(self):
        for arg in self.arguments:
            # TODO: Generate help message
            return

    @property
    def parsed(self):
        if not self._parsed:
            self._parsed = {a.name: a.value for a in self.arguments}
        return self._parsed

    def add_argument(self, arg: Union[Argument, dict]) -> None:
        if isinstance(arg, dict):
            arg = Argument(**arg)
        self.arguments.append(arg)
        self._arg_lookup[arg.name] = arg

    def parse_args(self, args: Optional[list]) -> dict:
        parsed = {}
        if not args:
            args = argv[1:]
        for arg in args:
            name, value = re.match(self.format, arg).groups()
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
        self._parsed = parsed
