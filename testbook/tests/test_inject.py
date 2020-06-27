import pytest

from ..testbook import testbook


@pytest.fixture(scope='module')
def notebook():
    with testbook('testbook/tests/resources/inject.ipynb', execute=True) as tb:
        yield tb


def inject_helper(*args, **kwargs):
    pass


@pytest.mark.parametrize(
    "args, kwargs",
    [
        (None, None),
        ([1, 2], None),
        ((1, 2), None),
        ((True, False), None),
        (['a', 'b'], None),
        ([1.1, float('nan'), float('inf'), float('-inf')], None),
        ([{'key1': 'value1'}, {'key2': 'value2'}], None),
        ((1, 2, False), {'key2': 'value2'}),
        ((None, None, False), {'key2': 'value2'}),
    ],
)
def test_inject(args, kwargs, notebook):
    assert notebook.inject(inject_helper, args=args, kwargs=kwargs, pop=True)


@pytest.mark.parametrize(
    "code_block, expected_text",
    [
        (
            '''
            def foo():
                print('I ran in the code block')
            foo()
        ''',
            "I ran in the code block",
        ),
        (
            '''
            def foo(arg):
                print(f'You passed {arg}')
            foo('bar')
        ''',
            "You passed bar",
        ),
    ],
)
def test_inject_code_block(code_block, expected_text, notebook):
    assert notebook.inject(code_block, pop=True).output_text == expected_text


def test_inject_raises_exception(notebook):
    values = [3, {'key': 'value'}, ['a', 'b', 'c'], (1, 2, 3), {1, 2, 3}]

    for value in values:
        with pytest.raises(TypeError):
            notebook.inject(value)


def test_inject_before_after(notebook):
    notebook.inject("say_hello()", run=False, after="hello")
    assert notebook.cells[notebook._cell_index("hello") + 1].source == "say_hello()"

    notebook.inject("say_bye()", before="hello")
    assert notebook.cells[notebook._cell_index("hello") - 1].source == "say_bye()"

    with pytest.raises(ValueError):
        notebook.inject("say_hello()", before="hello", after="bye")


def test_inject_pop(notebook):
    assert notebook.inject("1+1", pop=True).execute_result == [{'text/plain': '2'}]
    assert notebook.cells[-1].source != "1+1"
