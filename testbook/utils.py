import random
import string


def random_varname(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
