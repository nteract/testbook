class TestbookError(Exception):
    pass


class TestbookCellTagNotFoundError(TestbookError):
    """Raised when cell tag is not declared in notebook"""

    pass
