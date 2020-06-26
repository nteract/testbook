import pytest

from ..testbook import testbook


def helper_1():
    print("I ran in the kernel")


def helper_2(arg1, arg2):
    print(f"You passed {arg1} and {arg2}")


@pytest.mark.parametrize(
    "helper_func, args, expected_text",
    [
        (helper_1, None, "I ran in the kernel"),
        (helper_2, [1, 2], "You passed 1 and 2"),
        (helper_2, ['a', 'b'], "You passed a and b"),
        (helper_2, [[1, 2], 'b'], "You passed [1, 2] and b"),
        (
            helper_2,
            [{'key1': 'value1'}, {'key2': 'value2'}],
            "You passed {'key1': 'value1'} and {'key2': 'value2'}",
        ),
    ],
)
def test_inject(helper_func, args, expected_text):

    with testbook('testbook/tests/resources/foo.ipynb') as notebook:
        assert notebook.inject(helper_func, args).output_text == expected_text


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
def test_inject_code_block(code_block, expected_text):
    with testbook('testbook/tests/resources/foo.ipynb') as notebook:
        assert notebook.inject(code_block).output_text == expected_text


def test_inject_raises_exception():
    with testbook('testbook/tests/resources/foo.ipynb') as notebook:

        values = [3, {'key': 'value'}, ['a', 'b', 'c'], (1, 2, 3), {1, 2, 3}]

        for value in values:
            with pytest.raises(TypeError):
                notebook.inject(value)


def test_inject_before_after():
    with testbook('testbook/tests/resources/inject.ipynb', execute=['hello', 'bye']) as notebook:
        notebook.inject("say_hello()", run=False, after="hello")
        assert notebook.cells[notebook._cell_index("hello") + 1].source == "say_hello()"

        notebook.inject("say_bye()", before="hello")
        assert notebook.cells[notebook._cell_index("hello") - 1].source == "say_bye()"

        with pytest.raises(ValueError):
            notebook.inject("say_hello()", before="hello", after="bye")
