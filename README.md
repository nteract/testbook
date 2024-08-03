[![Build Status](https://github.com/nteract/testbook/workflows/CI/badge.svg)](https://github.com/nteract/testbook/actions)
[![image](https://codecov.io/github/nteract/testbook/coverage.svg?branch=master)](https://codecov.io/github/nteract/testbook?branch=master)
[![Documentation Status](https://readthedocs.org/projects/testbook/badge/?version=latest)](https://testbook.readthedocs.io/en/latest/?badge=latest)
[![image](https://img.shields.io/pypi/v/testbook.svg)](https://pypi.python.org/pypi/testbook)
[![image](https://img.shields.io/pypi/l/testbook.svg)](https://github.com/astral-sh/testbook/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/testbook.svg)](https://pypi.python.org/pypi/testbook)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# testbook

**testbook** is a unit testing framework extension for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself.
However, testbook will allow for unit tests to be run against notebooks in separate test files,
hence treating .ipynb files as .py files.

testbook helps you set up **conventional unit tests for your Jupyter Notebooks**.

Here is an example of a unit test written using testbook

Consider the following code cell in a Jupyter Notebook `example_notebook.ipynb`:

```python
def func(a, b):
   return a + b
```

You would write a unit test using `testbook` in a Python file `example_test.py` as follows:

```python
# example_test.py
from testbook import testbook


@testbook('/path/to/example_notebook.ipynb', execute=True)
def test_func(tb):
   func = tb.get("func")

   assert func(1, 2) == 3
```

Then [pytest](https://github.com/pytest-dev/pytest) can be used to run the test:

```{code-block} bash
pytest example_test.py
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
