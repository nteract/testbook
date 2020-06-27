import pytest

from ..testbook import testbook
from ..exceptions import TestbookAttributeError, TestbookSerializeError


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/reference.ipynb', execute=True) as tb:
        yield tb


def test_create_reference(notebook):
    spam = notebook.ref("spam")
    assert repr(spam) == "[1, 2, 3]"
    assert spam._type == 'list'
    assert spam.resolve() == [1, 2, 3]


def test_eq_in_notebook(notebook):
    spam = notebook.ref("spam")
    spam.append(4)
    assert spam == [1, 2, 3, 4]

    spam.remove(4)


def test_function_call(notebook):
    double = notebook.ref("double")
    assert double([1, 2, 3]) == [2, 4, 6]


def test_function_call_with_ref_object(notebook):
    double, spam = notebook.ref("double"), notebook.ref("spam")

    assert double(spam) == [2, 4, 6]


def test_reference(notebook):
    Foo = notebook.ref("Foo")

    # Check that when a non-serializeable object is returned, it returns
    # a reference to that object instead
    f = Foo('bar')

    assert repr(f) == "<Foo value='bar'>"

    # Valid attribute access
    assert f.say_hello

    # Invalid attribute access
    with pytest.raises(TestbookAttributeError):
        f.does_not_exist

    assert f.say_hello() == 'Hello bar!'

    # non JSON-serializeable output
    with pytest.raises(TestbookSerializeError):
        f.resolve()
