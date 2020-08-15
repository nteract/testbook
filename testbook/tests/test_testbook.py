from ..testbook import testbook


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
