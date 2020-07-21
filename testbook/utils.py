import random
import string


def random_varname(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def all_subclasses(klass):
    for subklass in klass.__subclasses__():
        yield subklass
        yield from all_subclasses(subklass)
