# Welcome to testbook

[![Github-CI][github-badge]][github-link]
[![Github-CI][github-ci]][github-ci-link]
[![Coverage Status][codecov-badge]][codecov-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![PyPI][pypi-badge]][pypi-link]
[![image](https://img.shields.io/pypi/v/testbook.svg)](https://pypi.python.org/pypi/testbook)
[![image](https://img.shields.io/pypi/l/testbook.svg)](https://github.com/astral-sh/testbook/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/testbook.svg)](https://pypi.python.org/pypi/testbook)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

**testbook** is a unit testing framework for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself. However, testbook will allow for unit tests to be run against notebooks in separate test files, hence treating `.ipynb` files as `.py` files.

Here is an example of a unit test written using testbook

Consider the following code cell in a Jupyter Notebook:

```{code-block} python
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

---

## Features

- Write conventional unit tests for Jupyter Notebooks
- [Execute all or some specific cells before unit test](usage/index.md#using-execute-to-control-which-cells-are-executed-before-test)
- [Share kernel context across multiple tests](usage/index.md#share-kernel-context-across-multiple-tests) (using pytest fixtures)
- [Support for patching objects](usage/index.md#support-for-patching-objects)
- Inject code into Jupyter notebooks
- Works with any unit testing library - unittest, pytest or nose

## Documentation

```{toctree}
:maxdepth: 3



getting-started/index.md
usage/index.md
examples/index.md
reference/index.rst
changelog.md
```

[github-ci]: https://github.com/nteract/testbook/workflows/CI/badge.svg
[github-ci-link]: https://github.com/nteract/testbook/actions
[github-link]: https://github.com/nteract/testbook
[rtd-badge]: https://readthedocs.org/projects/testbook/badge/?version=latest
[rtd-link]: https://testbook.readthedocs.io/en/latest/?badge=latest
[codecov-badge]: https://codecov.io/gh/nteract/testbook/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/nteract/testbook
[github-badge]: https://img.shields.io/github/stars/nteract/testbook?label=github
[pypi-badge]: https://img.shields.io/pypi/v/testbook.svg
[pypi-link]: https://pypi.org/project/testbook/
