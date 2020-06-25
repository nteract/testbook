from ..testbook import testbook


@testbook('testbook/tests/resources/inject.ipynb', execute=True)
def test_execute_all(tb):
    for cell in tb.cells[:-1]:
        assert cell.execution_count
