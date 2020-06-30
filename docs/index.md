---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Welcome to testbook

[![Github-CI][github-badge]][github-link]
[![Github-CI][github-ci]][github-ci-link]
[![Coverage Status][codecov-badge]][codecov-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![PyPI][pypi-badge]][pypi-link]
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

**testbook** is a unit testing framework for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself. However, testbook will allow for unit tests to be run against notebooks in separate test files, hence treating `.ipynb` files as `.py` files.

Here is an example of a unit test written using testbook

Consider the following code cell in a Jupyter Notebook:

```{code-cell} ipython3
def func(a, b):
   return a + b
```

You would write a unit test using `testbook` in a Python file as follows:

```python
import testbook


@testbook.testbook('/path/to/notebook.ipynb', execute=True)
def test_func(tb):
   func = tb.ref("func")

   assert func(1, 2) == 3
```

---

## Features

- Write conventional unit tests for Jupyter Notebooks
- [Execute all or some specific cells before unit test](usage/index.html#using-execute-to-control-which-cells-are-executed-before-test)
- [Share kernel context across multiple tests](usage/index.html#share-kernel-context-across-multiple-tests) (using pytest fixtures)
- Inject code into Jupyter notebooks
- Works with any unit testing library - unittest, pytest or nose

## Documentation

```{toctree}
:maxdepth: 3



getting-started/index.md
usage/index.md
reference/index.rst
changelog.md
```

[github-ci]: https://github.com/nteract/testbook/workflows/CI/badge.svg
[github-ci-link]: https://github.com/nteract/testbook/actions
[github-link]: https://github.com/nteract/testbook
[rtd-badge]: https://readthedocs.org/projects/testbook/badge/?version=latest
[rtd-link]: https://test-book.readthedocs.io/en/latest/?badge=latest
[codecov-badge]: https://codecov.io/gh/nteract/testbook/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/nteract/testbook
[github-badge]: https://img.shields.io/github/stars/nteract/testbook?label=github
[pypi-badge]: https://img.shields.io/pypi/v/nteract-testbook.svg
[pypi-link]: https://pypi.org/project/nteract-testbook/
