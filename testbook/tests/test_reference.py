import pytest

from ..testbook import testbook
from ..exceptions import TestbookAttributeError, TestbookSerializeError


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/reference.ipynb', execute=True) as tb:
        yield tb


def test_create_reference(notebook):
    a = notebook.ref("a")
    assert repr(a) == "'[1, 2, 3]'"


def test_create_reference_resolve(notebook):
    a = notebook.ref("a")
    assert a.resolve() == [1, 2, 3]


def test_notebook_get_value(notebook):
    a = notebook.get("a")
    assert a == [1, 2, 3]


def test_eq_in_notebook(notebook):
    a = notebook.ref("a")
    a.append(4)
    assert a.resolve() == [1, 2, 3, 4]


def test_eq_in_notebook_ref(notebook):
    a, b = notebook.ref("a"), notebook.ref("b")
    assert a.resolve()[:3] == b


def test_function_call(notebook):
    double = notebook.ref("double")
    assert double([1, 2, 3]) == [2, 4, 6]


def test_function_call_with_ref_object(notebook):
    double, a = notebook.ref("double"), notebook.ref("a")
    # a.append(4) above applied to the referenced "a" and therefore is
    # reflected here
    assert double(a) == [2, 4, 6, 8]


def test_nontrivial_pickling(notebook):
    Foo = notebook.ref("Foo")
    f = Foo("bar")
    assert repr(f) == "<Foo value='bar'>"
    assert(f.say_hello() == "Hello bar!")