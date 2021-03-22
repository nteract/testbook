class TestbookError(Exception):
    """Generic Testbook exception class"""
    __test__ = False


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
    __test__ = False


class TestbookRuntimeError(RuntimeError):
    __test__ = False

    def __init__(self, evalue, traceback, eclass=None):
        super().__init__(evalue)
        self.evalue = evalue
        self.traceback = traceback
        self.eclass = eclass

    def __str__(self):  # pragma: no cover
        return str(self.traceback)

    def __repr__(self):  # pragma: no cover
        return str(self.traceback)
