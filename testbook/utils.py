import random
import string


def random_varname(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
