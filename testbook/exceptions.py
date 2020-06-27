class TestbookError(Exception):
    """Generic Testbook exception class"""

    pass


class TestbookCellTagNotFoundError(TestbookError):
    """Raised when cell tag is not declared in notebook"""

    pass


class TestbookSerializeError(TestbookError):
    """Raised when output cannot be JSON serialized"""

    pass


class TestbookExecuteResultNotFoundError(TestbookError):
    """Raised when there is no execute_result"""

    pass


class TestbookAttributeError(AttributeError):
    pass
