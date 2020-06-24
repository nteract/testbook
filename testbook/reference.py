from .exceptions import TestbookSerializeError


class TestbookObjectReference:
    def __init__(self, tb, name):
        self.tb = tb
        self.name: str = name


class TestbookVariableReference(TestbookObjectReference):
    def __eq__(self, rhs):
        return self.tb._assert_in_notebook(self.name, rhs)

    def __repr__(self):
        return f"<TestbookVariableReference name='{self.name}' id={id(self)}>"

    @property
    def value(self):
        try:
            return self.tb.value(self.name)
        except ValueError as e:
            raise TestbookSerializeError("cannot JSON serialize variable") from e


class TestbookCallableReference(TestbookObjectReference):
    def __repr__(self):
        return f"<TestbookCallableReference name='{self.name}' id={id(self)}>"

    def __call__(self, *args, **kwargs):
        code = self.tb._construct_call_code(self.name, args, kwargs)
        return self.tb.value(code)
