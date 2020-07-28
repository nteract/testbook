import pytest

from ..testbook import testbook
from nbclient.exceptions import CellExecutionError
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
    try:
        notebook.inject("1/0", pop=True)
    except TestbookRuntimeError as e:
        assert e.nbexception == ZeroDivisionError


def test_testbook_with_execute(notebook):
    notebook.execute_cell('execute_foo')
    assert notebook.cell_output_text('execute_foo') == 'foo'


def test_testbook_with_execute_context_manager(notebook):
    notebook.execute_cell('execute_foo')
    assert notebook.cell_output_text('execute_foo') == 'foo'


@testbook('testbook/tests/resources/exception.ipynb', execute=True)
def test_raise_exception(tb):
    try:
        tb.ref("raise_my_exception")()
    except TestbookRuntimeError as e:
        assert e.nbexception == CellExecutionError
