[![Documentation Status](https://readthedocs.org/projects/test-book/badge/?version=latest)](https://test-book.readthedocs.io/en/latest/?badge=latest)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# TestBook

**testbook** is a unit testing framework extension for testing code in Jupyter Notebooks.

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself.
However, testbook will allow for unit tests to be run against notebooks in separate test files,
hence treating .ipynb files as .py files.

testbook helps you set up **conventional unit tests for your Jupyter Notebooks**.

Here is an example of a unit test written using testbook:

```python
@testbook.notebook_loader('/path/to/notebook.ipynb')
def test_notebook(notebook):
    notebook.execute_cell('cell-tag')
    assert notebook.cell_output_text('cell-tag') == 'hello world'
```

The above snippet demonstrates `notebook_loader` used in a decorator pattern, it can also
be used in the context manager style as follows:

```python
def test_notebook():
    with testbook.notebook_loader('/path/to/notebook.ipynb') as notebook:
        notebook.execute_cell('cell-tag')
        assert notebook.cell_output_text('cell-tag') == 'hello world'
```

## Documentation

See [readthedocs](https://test-book.readthedocs.io/en/latest/) for more in-depth details.

## Development Guide

Read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to setup a local development environment and make code changes back to TestBook.
