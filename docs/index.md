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

**testbook** is a unit testing framework for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself. However, testbook will allow for unit tests to be run against notebooks in separate test files, hence treating `.ipynb` files as `.py` files.

An example of a unit test written using testbook

Consider the following code cell in a Jupyter Notebook:

```{code-cell} ipython3
def sum(a, b):
   return a + b
```

You would write a unit test using `testbook` in a Python file as follows:

```python
import testbook


@testbook.testbook('/path/to/notebook.ipynb', execute='sum-cell')
def test_notebook(tb):
   sum = tb.ref("sum")

   assert sum(1, 2) == 3
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
```
