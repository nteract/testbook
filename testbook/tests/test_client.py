import pytest
from textwrap import dedent

from ..testbook import testbook
from ..client import TestbookNotebookClient
from ..exceptions import TestbookCellTagNotFoundError, TestbookExecuteResultNotFoundError


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/inject.ipynb', execute=True) as tb:
        yield tb


@pytest.mark.parametrize("cell_index_args, expected_result", [(2, 2), ('hello', 1)])
def test_cell_index(cell_index_args, expected_result, notebook):
    assert notebook._cell_index(cell_index_args) == expected_result


@pytest.mark.parametrize(
    "cell_index_args, expected_error",
    [([1, 2, 3], TypeError), ('non-existent-tag', TestbookCellTagNotFoundError)],
)
def test_cell_index_raises_error(cell_index_args, expected_error, notebook):
    with pytest.raises(expected_error):
        notebook._cell_index(cell_index_args)


@pytest.mark.parametrize(
    "var_name, expected_result",
    [
        ('sample_dict', {'foo': 'bar'}),
        ('sample_list', ['foo', 'bar']),
        ('sample_list + ["hello world"]', ['foo', 'bar', 'hello world']),
        ('sample_int', 42),
        ('sample_int * 2', 84),
        ('sample_str', 'hello world'),
        ('sample_str + " foo"', 'hello world foo'),
    ],
)
def test_value(var_name, expected_result, notebook):
    assert notebook.value(var_name) == expected_result


@pytest.mark.parametrize(
    "code", [('sample_int *= 2'), ('print(sample_int)'), ('')],
)
def test_value_raises_error(code, notebook):
    with pytest.raises(TestbookExecuteResultNotFoundError):
        notebook.value(code)


@pytest.mark.parametrize(
    "cell, expected_result",
    [
        (
            {
                "cell_type": "code",
                "execution_count": 9,
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": "hello world\n" "foo\n" "bar\n",
                    },
                ],
            },
            """
            hello world
            foo
            bar
            """,
        ),
        ({"cell_type": "code", "execution_count": 9, "metadata": {}, "outputs": []}, ""),
    ],
)
def test_output_text(cell, expected_result):
    assert TestbookNotebookClient._output_text(cell) == dedent(expected_result).strip()


@pytest.mark.parametrize(
    "cell", [{}, {"cell_type": "markdown", "metadata": {}, "source": ["# Hello"]}]
)
def test_output_text_raises_error(cell):
    with pytest.raises(ValueError):
        assert TestbookNotebookClient._output_text(cell)
