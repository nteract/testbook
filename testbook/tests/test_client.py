import pytest

from testbook import notebook_loader
from testbook.exceptions import CellTagNotFoundError


@pytest.mark.parametrize("get_call_index_args, expected_result", [(2, 2), ('hello', 1)])
def test_get_cell_index(get_call_index_args, expected_result):
    with notebook_loader('testbook/tests/resources/inject.ipynb') as notebook:
        assert notebook._get_cell_index(get_call_index_args) == expected_result


@pytest.mark.parametrize(
    "get_call_index_args, expected_error",
    [([1, 2, 3], TypeError), ('non-existent-tag', CellTagNotFoundError)],
)
def test_get_cell_index_raises_error(get_call_index_args, expected_error):
    with notebook_loader('testbook/tests/resources/inject.ipynb') as notebook:
        with pytest.raises(expected_error):
            notebook._get_cell_index(get_call_index_args)
