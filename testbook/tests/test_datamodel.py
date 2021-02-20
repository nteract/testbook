import pytest

from ..testbook import testbook


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/datamodel.ipynb', execute=True) as tb:
        yield tb


def test_len(notebook):
    mylist = notebook.ref("mylist")

    assert len(mylist) == 5


def test_iter(notebook):
    mylist = notebook.ref("mylist")

    expected = []
    for x in mylist:
        expected.append(x)

    assert mylist == expected


def test_getitem(notebook):
    mylist = notebook.ref("mylist")
    mylist.append(6)

    assert mylist[-1] == 6
    assert mylist.__getitem__(-1) == 6


def test_getitem_raisesIndexError(notebook):
    mylist = notebook.ref("mylist")

    with pytest.raises(IndexError):
        mylist[100]


def test_getitem_raisesTypeError(notebook):
    mylist = notebook.ref("mylist")

    with pytest.raises(TypeError):
        mylist['hello']


def test_setitem(notebook):
    notebook.inject("mydict = {'key1': 'value1', 'key2': 'value1'}")
    mydict = notebook.ref("mydict")

    mydict['key3'] = 'value3'
    assert mydict['key3'] == 'value3'

    mylist = notebook.ref("mylist")
    mylist[2] = 10
    assert mylist[2] == 10


def test_setitem_raisesIndexError(notebook):
    mylist = notebook.ref("mylist")

    with pytest.raises(IndexError):
        mylist.__setitem__(10, 100)


def test_setitem_raisesTypeError(notebook):
    mylist = notebook.ref("mylist")

    with pytest.raises(TypeError):
        mylist.__setitem__('key', 10)


def test_contains(notebook):
    notebook.inject("mydict = {'key1': 'value1', 'key2': 'value1'}")
    mydict = notebook.ref("mydict")

    assert 'key1' in mydict
    assert 'key2' in mydict
    assert mydict.__contains__('key1')
    assert mydict.__contains__('key2')
