import pytest

from testbook import notebook_loader


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
def test_inject(helper_func, args, expected_text, notebook_loader):

    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
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
def test_inject_code_block(code_block, expected_text, notebook_loader):
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        assert notebook.inject(code_block).output_text == expected_text


def test_inject_raises_exception(notebook_loader):
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:

        values = [3, {'key': 'value'}, ['a', 'b', 'c'], (1, 2, 3), {1, 2, 3}]

        for value in values:
            with pytest.raises(TypeError):
                notebook.inject(value)


@pytest.mark.parametrize(
    "prerun, code_block, expected_text",
    [
        (
            0,
            '''
            print(f"{foo} {bar}")
            ''',
            "Hello World",
        ),
        (
            [1, 2],
            '''
            say_hello()
            say_bye()
            ''',
            "Hello there\nBye",
        ),
        (
            ['hello', 'bye'],
            '''
            say_hello()
            say_bye()
            ''',
            "Hello there\nBye",
        ),
    ],
)
def test_inject_with_prerun(prerun, code_block, expected_text, notebook_loader):
    with notebook_loader('testbook/tests/resources/inject.ipynb') as notebook:
        assert notebook.inject(code_block, prerun=prerun).output_text == expected_text
