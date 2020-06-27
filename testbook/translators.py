"""Sourced from https://github.com/nteract/papermill/blob/master/papermill/translators.py"""
import math
import sys

from .reference import TestbookObjectReference


class Translator(object):
    @classmethod
    def translate_raw_str(cls, val):
        """Reusable by most interpreters"""
        return '{}'.format(val)

    @classmethod
    def translate_escaped_str(cls, str_val):
        """Reusable by most interpreters"""
        if isinstance(str_val, str):
            str_val = str_val.encode('unicode_escape')
            if sys.version_info >= (3, 0):
                str_val = str_val.decode('utf-8')
            str_val = str_val.replace('"', r'\"')
        return '"{}"'.format(str_val)

    @classmethod
    def translate_str(cls, val):
        """Default behavior for translation"""
        return cls.translate_escaped_str(val)

    @classmethod
    def translate_none(cls, val):
        """Default behavior for translation"""
        return cls.translate_raw_str(val)

    @classmethod
    def translate_int(cls, val):
        """Default behavior for translation"""
        return cls.translate_raw_str(val)

    @classmethod
    def translate_float(cls, val):
        """Default behavior for translation"""
        return cls.translate_raw_str(val)

    @classmethod
    def translate_bool(cls, val):
        """Default behavior for translation"""
        return 'true' if val else 'false'

    @classmethod
    def translate_dict(cls, val):
        raise NotImplementedError('dict type translation not implemented for {}'.format(cls))

    @classmethod
    def translate_list(cls, val):
        raise NotImplementedError('list type translation not implemented for {}'.format(cls))

    @classmethod
    def translate(cls, val):
        """Translate each of the standard json/yaml types to appropriate objects."""
        if val is None:
            return cls.translate_none(val)
        elif isinstance(val, str):
            return cls.translate_str(val)
        # Needs to be before integer checks
        elif isinstance(val, bool):
            return cls.translate_bool(val)
        elif isinstance(val, int):
            return cls.translate_int(val)
        elif isinstance(val, float):
            return cls.translate_float(val)
        elif isinstance(val, dict):
            return cls.translate_dict(val)
        elif isinstance(val, list):
            return cls.translate_list(val)
        elif isinstance(val, tuple):
            return cls.translate_tuple(val)
        elif isinstance(val, TestbookObjectReference):
            return val.name

        # Use this generic translation as a last resort
        return cls.translate_escaped_str(val)

    @classmethod
    def comment(cls, cmt_str):
        raise NotImplementedError('comment translation not implemented for {}'.format(cls))

    @classmethod
    def assign(cls, name, str_val):
        return '{} = {}'.format(name, str_val)


class PythonTranslator(Translator):
    @classmethod
    def translate_float(cls, val):
        if math.isfinite(val):
            return cls.translate_raw_str(val)
        elif math.isnan(val):
            return "float('nan')"
        elif val < 0:
            return "float('-inf')"
        else:
            return "float('inf')"

    @classmethod
    def translate_bool(cls, val):
        return cls.translate_raw_str(val)

    @classmethod
    def translate_dict(cls, val):
        escaped = ', '.join(
            ["{}: {}".format(cls.translate_str(k), cls.translate(v)) for k, v in val.items()]
        )
        return '{{{}}}'.format(escaped)

    @classmethod
    def translate_list(cls, val):
        escaped = ', '.join([cls.translate(v) for v in val])
        return '[{}]'.format(escaped)

    @classmethod
    def translate_tuple(cls, val):
        escaped = ', '.join([cls.translate(v) for v in val]) + ', '
        return '({})'.format(escaped)
