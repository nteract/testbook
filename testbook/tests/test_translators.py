"""Sourced from https://github.com/nteract/papermill/blob/master/papermill/tests/test_translators.py"""
import pytest

from .. import translators


class Foo:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "<Foo val='{val}'>".format(val=self.val)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("foo", '"foo"'),
        ('{"foo": "bar"}', '"{\\"foo\\": \\"bar\\"}"'),
        ({"foo": "bar"}, '{"foo": "bar"}'),
        ({"foo": '"bar"'}, '{"foo": "\\"bar\\""}'),
        ({"foo": ["bar"]}, '{"foo": ["bar"]}'),
        ({"foo": {"bar": "baz"}}, '{"foo": {"bar": "baz"}}'),
        ({"foo": {"bar": '"baz"'}}, '{"foo": {"bar": "\\"baz\\""}}'),
        (["foo"], '["foo"]'),
        (["foo", '"bar"'], '["foo", "\\"bar\\""]'),
        ([{"foo": "bar"}], '[{"foo": "bar"}]'),
        ([{"foo": '"bar"'}], '[{"foo": "\\"bar\\""}]'),
        (12345, '12345'),
        (-54321, '-54321'),
        (1.2345, '1.2345'),
        (-5432.1, '-5432.1'),
        (float('nan'), "float('nan')"),
        (float('-inf'), "float('-inf')"),
        (float('inf'), "float('inf')"),
        (True, 'True'),
        (False, 'False'),
        (None, 'None'),
        (Foo('bar'), '''"<Foo val='bar'>"'''),
    ],
)
def test_translate_type_python(test_input, expected):
    assert translators.PythonTranslator.translate(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [(3.14, "3.14"), (False, "false"), (True, "true")])
def test_translate_float(test_input, expected):
    assert translators.Translator.translate(test_input) == expected


def test_translate_assign():
    assert translators.Translator.assign('var1', [1, 2, 3]) == "var1 = [1, 2, 3]"
