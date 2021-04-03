import pytest

from ..testbook import testbook
from ..exceptions import TestbookAttributeError, TestbookSerializeError


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/reference.ipynb', execute=True) as tb:
        yield tb


def test_create_reference(notebook):
    a = notebook.ref("a")
    assert repr(a) == "[1, 2, 3]"


def test_create_reference_getitem(notebook):
    a = notebook["a"]
    assert repr(a) == "[1, 2, 3]"


def test_create_reference_get(notebook):
    a = notebook.get("a")
    assert repr(a) == "[1, 2, 3]"


def test_eq_in_notebook(notebook):
    a = notebook.ref("a")
    a.append(4)
    assert a == [1, 2, 3, 4]


def test_eq_in_notebook_ref(notebook):
    a, b = notebook.ref("a"), notebook.ref("b")
    assert a == b


def test_function_call(notebook):
    double = notebook.ref("double")
    assert double([1, 2, 3]) == [2, 4, 6]


def test_function_call_with_ref_object(notebook):
    double, a = notebook.ref("double"), notebook.ref("a")

    assert double(a) == [2, 4, 6]


def test_reference(notebook):
    Foo = notebook.ref("Foo")

    # Check that when a non-serializeable object is returned, it returns
    # a reference to that object instead
    f = Foo('bar')

    assert repr(f) == "\"<Foo value='bar'>\""

    # Valid attribute access
    assert f.say_hello()

    # Invalid attribute access
    with pytest.raises(TestbookAttributeError):
        f.does_not_exist

    assert f.say_hello() == 'Hello bar!'

    # non JSON-serializeable output
    with pytest.raises(TestbookSerializeError):
        f.resolve()
