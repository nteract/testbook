Welcome to testbook
===================

**testbook** is a unit testing framework extension for testing code in Jupyter Notebooks.

------

Previous attempts at unit testing notebooks involved writing the tests in the notebook itself. 
However, testbook will allow for unit tests to be run against notebooks in separate test files, 
hence treating .ipynb files as .py files.


testbook helps you set up **conventional unit tests for your Jupyter Notebooks**.

Here is an example of a unit test written using testbook:

.. code-block:: python

   @testbook.notebook_loader('/path/to/notebook.ipynb')
   def test_notebook(notebook):
       notebook.execute_cell('cell-tag')
       assert notebook.cell_output_text('cell-tag') == 'hello world'

The above snippet demonstrates ``notebook_loader`` used in a decorator pattern, it can also 
be used in the context manager style as follows:

.. code-block:: python

   def test_notebook():
       with testbook.notebook_loader('/path/to/notebook.ipynb') as notebook:
           notebook.execute_cell('cell-tag')
           assert notebook.cell_output_text('cell-tag') == 'hello world'


-----------

Features
--------

- **Pre-run cells before test execution**


.. code-block:: python

   @testbook.notebook_loader('/path/to/notebook.ipynb', prerun=['cell1', 'cell2'])
   def test_notebook_with_prerun(notebook):
      assert notebook.cell_output_text('cell3') == 'hello world'

**Note:** ``cell1``, ``cell2`` and ``cell3`` are Jupyter Notebook cell tags.


- **Share kernel context across multiple tests**

.. code-block:: python

   notebook_context = testbook.notebook_loader('notebook.ipynb', prerun=['tag1', 'tag2', 'tag3'])


   def test_notebook():
      with notebook_context() as notebook:
         assert notebook.cell_output_text('tag4') == 'hello world'

   def test_notebook_1():
      with notebook_context() as notebook:
         assert notebook.cell_output_text('tag5') == 'hello world'


- **Inject functions**

.. code-block:: python

   def foo(name):
      print(f"hello {name}")

   def test_notebook():
      with testbook.notebook_loader('notebook.ipynb') as notebook:
          assert notebook.inject(foo, args=['world']).output_text == 'hello world'


- **Inject code snippets**

.. code-block:: python

   def test_notebook():
      with testbook.notebook_loader('notebook.ipynb') as notebook:
          code_snippet = """
              print('hello world')
          """
          assert notebook.inject(code_snippet).output_text == 'hello world'
