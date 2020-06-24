import random
import string

from .translators import PythonTranslator


def random_varname(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def _construct_call_code(func_name, args=None, kwargs=None):
    return """
        {func_name}(*{args_list}, **{kwargs_dict})
        """.format(
        func_name=func_name,
        args_list=PythonTranslator.translate(args) if args else [],
        kwargs_dict=PythonTranslator.translate(args) if kwargs else {},
    )
