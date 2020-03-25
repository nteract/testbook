import pytest

from testbook import notebook


def test_notebook(notebook):
    with notebook('testbook/tests/resources/foo.ipynb') as nb:
        nb.execute_cell(1)

        assert nb.cell_output_text(1) == 'hello world\n[1, 2, 3]\n'
