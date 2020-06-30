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

# Installation and Getting Started

`testbook` is a unit testing framework for testing code in Jupyter Notebooks.

## Installing `testbook`

```{code-block} bash
pip install nteract-testbook
```

## Create your first test

Consider the following code cell in a Jupyter Notebook,

```{code-cell} ipython3
:tags: [hide-output]

def foo(x):
    return x + 1
```

Here is the unit test for it which must be written in a Python module (`.py` file).

```{code-block} python
from testbook import testbook

@testbook('/path/to/notebook.ipynb', execute=True)
def test_foo(tb):
    foo = tb.ref("foo")

    assert foo(2) == 3
```

That's it! You can now execute the test.

## General workflow when using testbook to write a unit test

1. Use `testbook.testbook` as a decorator or context manager to specify the path to the Jupyter Notebook. Passing `execute=True` will execute all the cells, and passing `execute=['cell-tag-1', 'cell-tag-2']` will only execute specific cells identified by cell tags.

2. Obtain references to objects under test using the `.ref` method.

3. Write the test!
