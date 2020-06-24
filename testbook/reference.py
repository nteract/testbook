class TestbookObjectReference:
    def __init__(self, tb, name):
        self.tb = tb
        self.name: str = name

    def __repr__(self):
        return f"<TestbookObjectReference name='{self.name}' id={id(self)}>"

    def __getattr__(self, name):
        return TestbookObjectReference(self.tb, f"{self.name}.{name}")

    def __eq__(self, rhs):
        return self.tb._assert_in_notebook(self.name, rhs)

    def __call__(self, *args, **kwargs):
        code = self.tb._construct_call_code(self.name, args, kwargs)
        return self.tb.value(code)

    def resolve(self):
        return self.tb.value(self.name, safe=False)
