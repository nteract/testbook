import nbformat

import pytest

from testbook.testbook import testbook


@testbook('testbook/tests/resources/inject.ipynb', execute=True)
def test_testbook_execute_all_cells(tb):
    for cell in tb.cells[:-1]:
        assert cell.execution_count


@testbook('testbook/tests/resources/inject.ipynb', execute='hello')
def test_testbook_class_decorator(tb):
    assert tb.inject("say_hello()")


@testbook('testbook/tests/resources/inject.ipynb')
def test_testbook_class_decorator_execute_none(tb):
    assert tb.code_cells_executed == 0


@testbook('testbook/tests/resources/inject.ipynb', execute=True)
def test_testbook_decorator_with_fixture(nb, tmp_path):
    assert True  # Check that the decorator accept to be passed along side a fixture


@testbook('testbook/tests/resources/inject.ipynb', execute=True)
@pytest.mark.parametrize("cell_index_args, expected_result", [(2, 2), ('hello', 1)])
def test_testbook_decorator_with_markers(nb, cell_index_args, expected_result):
    assert nb._cell_index(cell_index_args) == expected_result


@pytest.mark.parametrize("cell_index_args, expected_result", [(2, 2), ('hello', 1)])
@testbook('testbook/tests/resources/inject.ipynb', execute=True)
def test_testbook_decorator_with_markers_order_does_not_matter(nb, cell_index_args, expected_result):
    assert nb._cell_index(cell_index_args) == expected_result


def test_testbook_execute_all_cells_context_manager():
    with testbook('testbook/tests/resources/inject.ipynb', execute=True) as tb:
        for cell in tb.cells[:-1]:
            assert cell.execution_count


def test_testbook_class_decorator_context_manager():
    with testbook('testbook/tests/resources/inject.ipynb', execute='hello') as tb:
        assert tb.inject("say_hello()")


def test_testbook_class_decorator_execute_none_context_manager():
    with testbook('testbook/tests/resources/inject.ipynb') as tb:
        assert tb.code_cells_executed == 0


def test_testbook_with_file_object():
    f = open('testbook/tests/resources/inject.ipynb')

    with testbook(f) as tb:
        assert tb.code_cells_executed == 0

    f.close()


def test_testbook_with_notebook_node():
    nb = nbformat.read('testbook/tests/resources/inject.ipynb', as_version=4)

    with testbook(nb) as tb:
        assert tb.code_cells_executed == 0
