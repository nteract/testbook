[![Build Status](https://github.com/nteract/testbook/workflows/CI/badge.svg)](https://github.com/nteract/testbook/actions)
[![image](https://codecov.io/github/nteract/testbook/coverage.svg?branch=master)](https://codecov.io/github/nteract/testbook?branch=master)
[![Documentation Status](https://readthedocs.org/projects/testbook/badge/?version=latest)](https://testbook.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/testbook.svg)](https://pypi.org/project/testbook/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# testbook

**testbook** is a unit testing framework extension for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself.
However, testbook will allow for unit tests to be run against notebooks in separate test files,
hence treating .ipynb files as .py files.

testbook helps you set up **conventional unit tests for your Jupyter Notebooks**.

Here is an example of a unit test written using testbook

Consider the following code cell in a Jupyter Notebook:

```python
def func(a, b):
   return a + b
```

You would write a unit test using `testbook` in a Python file as follows:

```python
from testbook import testbook


@testbook('/path/to/notebook.ipynb', execute=True)
def test_func(tb):
   func = tb.get("func")

   assert func(1, 2) == 3
```

## Installing `testbook`

```{code-block} bash
pip install testbook
```

NOTE: This does not install any kernels for running your notebooks. You'll need to install in the same way you do for running the notebooks normally. Usually this is done with `pip install ipykernel`

Alternatively if you want all the same dev dependencies and the ipython kernel you can install these dependencies with:

```{code-block} bash
pip install testbook[dev]
```

## Documentation

See [readthedocs](https://testbook.readthedocs.io/en/latest/) for more in-depth details.

## Development Guide

Read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to setup a local development environment and make code changes back to testbook.
