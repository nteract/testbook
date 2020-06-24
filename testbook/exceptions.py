class TestbookError(Exception):
    pass


class TestbookCellTagNotFoundError(TestbookError):
    """Raised when cell tag is not declared in notebook"""

    pass


class TestbookSerializeError(TestbookError):
    """Raised when result cannot be JSON serialized"""

    pass
