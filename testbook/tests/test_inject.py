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
        (helper_2, [{'key1': 'value1'}, {'key2': 'value2'}], "You passed {'key1': 'value1'} and {'key2': 'value2'}"),
    ],
)
def test_inject(helper_func, args, expected_text, notebook_loader):

    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.inject(helper_func, args).assert_output_text(expected_text)
