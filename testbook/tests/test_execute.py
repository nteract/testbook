import pytest

from ..testbook import testbook
from ..exceptions import TestbookRuntimeError


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/foo.ipynb', execute=True) as tb:
        yield tb


def test_execute_cell(notebook):
    notebook.execute_cell(1)
    assert notebook.cell_output_text(1) == 'hello world\n[1, 2, 3]'

    notebook.execute_cell([2, 3])
    assert notebook.cell_output_text(3) == 'foo'


def test_execute_cell_tags(notebook):
    notebook.execute_cell('test1')
    assert notebook.cell_output_text('test1') == 'hello world\n[1, 2, 3]'

    notebook.execute_cell(['prepare_foo', 'execute_foo'])
    assert notebook.cell_output_text('execute_foo') == 'foo'


def test_execute_cell_raises_error(notebook):
    with pytest.raises(TestbookRuntimeError):
        try:
            notebook.inject("1/0", pop=True)
        except TestbookRuntimeError as e:
            assert e.eclass == ZeroDivisionError
            raise


def test_testbook_with_execute(notebook):
    notebook.execute_cell('execute_foo')
    assert notebook.cell_output_text('execute_foo') == 'foo'


def test_testbook_with_execute_context_manager(notebook):
    notebook.execute_cell('execute_foo')
    assert notebook.cell_output_text('execute_foo') == 'foo'


def test_testbook_range():
    with testbook('testbook/tests/resources/inject.ipynb') as tb:
        tb.execute_cell(range(4))
        assert tb.code_cells_executed == 4

    with testbook('testbook/tests/resources/inject.ipynb', execute=range(4)) as tb:
        assert tb.code_cells_executed == 4


@pytest.mark.parametrize("slice_params, expected_result", [(('hello', 'str'), 5), ((2, 5), 3),])
def test_testbook_slice(slice_params, expected_result):
    with testbook('testbook/tests/resources/inject.ipynb') as tb:
        tb.execute_cell(slice(*slice_params))
        assert tb.code_cells_executed == expected_result

    with testbook('testbook/tests/resources/inject.ipynb', execute=slice(*slice_params)) as tb:
        assert tb.code_cells_executed == expected_result


@testbook('testbook/tests/resources/exception.ipynb', execute=True)
def test_raise_exception(tb):
    with pytest.raises(TestbookRuntimeError):
        tb.ref("raise_my_exception")()
