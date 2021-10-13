Usage
===============

Installation
************

To get started, install ``bearparse``::

    $ pip install --upgrade bearparse

Getting Started
***************

Getting started is easy:

.. code-block:: python

    from bearparse import Argument, ArgumentParser

    # Create the parser
    parser = ArgumentParser(description="Program Description")
    parser.add_argument(Argument(name="arg", description="First Argument"))
    parser.add_argument(Argument(name="arg2", description="Required Argument", required=True))

    # Parse from argv
    args = parser.parse_args()

    print(args.parsed)

Advanced Usage
**************


Formatting
----------

You can use custom argument formatting for various needs:

.. code-block:: python

    from bearparse import Argument, ArgumentParser

    # Create the parser with a custom format of --key=value
    parser = ArgumentParser(description="Program Description", format=r"^--([\w]{1,})=(.*)$")
    parser.add_argument(Argument(name="arg", description="First Argument"))

    # Parse from argv
    args = parser.parse_args(["--arg=Test"])

    print(args.arg) # Test


Argument Types
--------------

:class:`bearparse.Argument` support types, and will automatically convert an argument into the specified type:

.. code-block:: python

    from bearparse import Argument, ArgumentParser

    # Create the parser
    parser = ArgumentParser(description="Program Description")
    parser.add_argument(Argument(name="arg", description="First Argument", type=int))
    parser.add_argument(Argument(name="arg2", description="Second Argument", type=str))

    # Parse from argv
    args = parser.parse_args(["arg=3", "arg2=4"])

    print(type(args.arg))  # <class 'int'>
    print(type(args.arg2))  # <class 'str'>


Parsers
-------

If you need to parse user input into a boolean, float, or int, there are build-in methods to handle this:

.. code-block:: python

    from bearparse import Argument, ArgumentParser
    from bearparse.parsers import bool_parser

    # Create the parser
    parser = ArgumentParser(description="Program Description")
    parser.add_argument(Argument(name="arg", description="First Argument", parser=bool_parser))

    # Parse from argv
    args = parser.parse_args(["arg=Yes"])

    print(args.arg)  # True

You can also implement custom parsers for handling unique situations:

.. code-block:: python

    from bearparse import Argument, ArgumentParser
    from bearparse.parsers import float_parser

    def ceil_parser(value):
        return ceil(float_parser(value))

    # Create the parser
    parser = ArgumentParser(description="Program Description")
    parser.add_argument(Argument(name="arg", description="First Argument", parser=ceil_parser))

    # Parse from argv
    args = parser.parse_args(["arg=3.2"])

    print(args.arg)  # 4
