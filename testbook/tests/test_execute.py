import pytest

from testbook import notebook_loader


def test_notebook(notebook_loader):
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.execute_cell(1)
        assert notebook.cell_output_text(1) == 'hello world\n[1, 2, 3]\n'

        notebook.execute_cell([2, 3])
        assert notebook.cell_output_text(3) == 'foo\n'
