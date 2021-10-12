# bearparse

![Python Unittests](https://github.com/zevaryx/bearparse/actions/workflows/python-package.yaml/badge.svg) [![codecov](https://codecov.io/gh/zevaryx/bearparse/main/graph/badge.svg?token=GG7DVUW7RJ)](https://codecov.io/gh/zevaryx/bearparse)

[![pipeline status](https://git.zevaryx.com/zevaryx/bearparse/badges/main/pipeline.svg)](https://git.zevaryx.com/zevaryx/bearparse/-/commits/main)
[![coverage report](https://git.zevaryx.com/zevaryx/bearparse/badges/main/coverage.svg)](https://git.zevaryx.com/zevaryx/bearparse/-/commits/main)

A custom argument parser for non-standard arguments. Useful for Appworx

## Purpose

To simplify

## Requirements

- Python 3.8+

## Usage

```py
from bearparse import Argument, ArgumentParser

# Create the parser
parser = ArgumentParser(description="Program Description")
parser.add_argument(Argument(name="arg", description="First Argument"))
parser.add_argument(Argument(name="arg2", description="Required Argument", required=True))

# Parse from argv
args = parser.parse_args()

print(args.parsed)
```
