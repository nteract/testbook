import pytest

from testbook import testbook
from testbook.exceptions import CellTagNotFoundError


@pytest.mark.parametrize("cell_index_args, expected_result", [(2, 2), ('hello', 1)])
def test_cell_index(cell_index_args, expected_result):
    with testbook('testbook/tests/resources/inject.ipynb') as notebook:
        assert notebook._cell_index(cell_index_args) == expected_result


@pytest.mark.parametrize(
    "cell_index_args, expected_error",
    [([1, 2, 3], TypeError), ('non-existent-tag', CellTagNotFoundError)],
)
def test_cell_index_raises_error(cell_index_args, expected_error):
    with testbook('testbook/tests/resources/inject.ipynb') as notebook:
        with pytest.raises(expected_error):
            notebook._cell_index(cell_index_args)
