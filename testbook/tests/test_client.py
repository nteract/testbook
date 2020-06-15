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


@pytest.mark.parametrize(
    "cell_tag, var_name, expected_result",
    [
        ('dict', 'sample_dict', {'foo': 'bar'}),
        ('list', 'sample_list', ['foo', 'bar']),
        ('list', 'sample_list + ["hello world"]', ['foo', 'bar', 'hello world']),
        ('int', 'sample_int', 42),
        ('int', 'sample_int * 2', 84),
        ('str', 'sample_str', 'hello world'),
        ('str', 'sample_str + " foo"', 'hello world foo'),
    ],
)
def test_value(cell_tag, var_name, expected_result):
    with testbook('testbook/tests/resources/inject.ipynb', prerun=cell_tag) as notebook:
        assert notebook.value(var_name) == expected_result


@pytest.mark.parametrize(
    "cell_tag, code", [('int', 'sample_int *= 2'), ('int', 'print(sample_int)'),],
)
def test_value_raises_error(cell_tag, code):
    with testbook('testbook/tests/resources/inject.ipynb', prerun=cell_tag) as notebook:
        with pytest.raises(ValueError):
            notebook.value(code)
