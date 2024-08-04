import random
import string


def random_varname(length=10):
    """
    Creates a random variable name as string of a given length.
    This is used in testbook to generate temporary variables within the notebook.

    Parameters
    ----------
        length (int)

    Returns:
    --------
        random variable name as string of given length
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def all_subclasses(klass):
    """
    This is a function that returns a generator.

    Inspects subclasses associated with a given class in a recursive manner
    and yields them, such that subclasses of subclasses will be yielded.

    Parameters:
    -----------
        klass
    """
    for subklass in klass.__subclasses__():
        yield subklass
        yield from all_subclasses(subklass)
