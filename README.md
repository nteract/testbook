testbook
===================

**testbook** is a unit testing framework extension for testing code in Jupyter Notebooks.

---

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself. 
However, testbook will allow for unit tests to be run against notebooks in separate test files, 
hence treating .ipynb files as .py files.


testbook helps you set up **conventional unit tests for your Jupyter Notebooks**.

Here is an example of a unit test written using testbook:

```python
import testbook

@testbook.notebook_loader('/path/to/notebook.ipynb')
def test_notebook(notebook):
    notebook.execute_cell('cell-1')
    assert notebook.cell_output_text('cell-1') == 'hello world'
```

The above snippet contains ``notebook_loader`` used in a decorator pattern, it can also 
be used in the context manager style as follows:

```python
import testbook

def test_notebook(notebook):
    with testbook.notebook_loader('/path/to/notebook.ipynb') as notebook:
        notebook.execute_cell('cell-1')
        assert notebook.cell_output_text('cell-1') == 'hello world'
```

---

Features
--------

- **Pre-run cells before test execution**


```python
from testbook import notebook_loader

@notebook_loader('/path/to/notebook.ipynb', prerun=['cell1', 'cell2'])
def test_notebook_with_prerun(notebook):
    assert notebook.cell_output_text('cell3') == 'hello world'
```

**Note:** ``cell1``, ``cell2`` and ``cell3`` are Jupyter Notebook cell tags.


- **Share kernel context across multiple tests**

```python
from testbook import notebook_loader

notebook_context = notebook_loader('notebook.ipynb', prerun=['tag1', 'tag2', 'tag3'])


def test_notebook():
    with notebook_context() as notebook:
        assert notebook.cell_output_text('tag4') == 'hello world'

def test_notebook_1():
    with notebook_context() as notebook:
        assert notebook.cell_output_text('tag5') == 'hello world'
```

- **Inject functions**

```python
from testbook import notebook_loader

def foo(name):
    print(f"hello {name}")

def test_notebook():
    with notebook_loader('notebook.ipynb') as notebook:
        assert notebook.inject(foo, args=['world']).output_text == 'hello world'
```

- **Inject code snippets**

```python
from testbook import notebook_loader

def test_notebook():
    with notebook_loader('notebook.ipynb') as notebook:
        code_snippet = """
            print('hello world')
        """
        assert notebook.inject(code_snippet).output_text == 'hello world'
```
   

