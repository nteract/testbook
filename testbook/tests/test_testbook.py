from ..testbook import testbook


def test_execute_all():
    with testbook('testbook/tests/resources/inject.ipynb', execute=True) as tb:
        for cell in tb.cells[:-1]:
            assert cell.execution_count
