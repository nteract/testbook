import pytest

from testbook import notebook_loader


def test_get_cell_index():
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        with pytest.raises(TypeError):
            notebook._get_cell_index(1)
