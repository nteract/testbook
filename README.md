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

## Features

- **Pre-run cells before test execution**

```python
@testbook.notebook_loader('/path/to/notebook.ipynb', prerun=['cell1', 'cell2'])
def test_notebook_with_prerun(notebook):
    assert notebook.cell_output_text('cell3') == 'hello world'
```

**Note:** `cell1`, `cell2` and `cell3` are Jupyter Notebook cell tags.

### **Share kernel context across multiple tests**

```python
notebook_context = testbook.notebook_loader('notebook.ipynb', prerun=['tag1', 'tag2', 'tag3'])

def test_notebook():
    with notebook_context() as notebook:
        assert notebook.cell_output_text('tag4') == 'hello world'

def test_notebook_1():
    with notebook_context() as notebook:
        assert notebook.cell_output_text('tag5') == 'hello world'
```

### **Inject functions**

```python
def foo(name):
    print(f"hello {name}")

def test_notebook():
    with testbook.notebook_loader('notebook.ipynb') as notebook:
        assert notebook.inject(foo, args=['world']).output_text == 'hello world'
```

### **Inject code snippets**

```python
def test_notebook():
    with testbook.notebook_loader('notebook.ipynb') as notebook:
        code_snippet = """
            print('hello world')
        """
        assert notebook.inject(code_snippet).output_text == 'hello world'
```
