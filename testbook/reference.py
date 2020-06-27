from .exceptions import (
    TestbookExecuteResultNotFoundError,
    TestbookAttributeError,
    TestbookSerializeError,
)


class TestbookObjectReference:
    def __init__(self, tb, name):
        self.tb = tb
        self.name: str = name

    @property
    def _type(self):
        return self.tb.value(f"type({self.name}).__name__")

    def __repr__(self):
        return self.tb.value(f"repr({self.name})")

    def __getattr__(self, name):
        if self.tb.value(f"hasattr({self.name}, '{name}')"):
            return TestbookObjectReference(self.tb, f"{self.name}.{name}")

        raise TestbookAttributeError(f"'{self._type}' object has no attribute {name}")

    def __eq__(self, rhs):
        return self.tb._eq_in_notebook(self.name, rhs)

    def __call__(self, *args, **kwargs):
        code = self.tb._construct_call_code(self.name, args, kwargs)
        try:
            return self.tb.value(code)
        except TestbookExecuteResultNotFoundError:
            # No return value from function call
            pass
        except TestbookSerializeError as e:
            return TestbookObjectReference(self.tb, e.save_varname)

    def resolve(self):
        return self.tb.value(self.name)
