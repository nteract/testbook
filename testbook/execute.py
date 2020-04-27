from contextlib import contextmanager

import nbformat
import pytest

from testbook.client import TestbookNotebookClient


@pytest.fixture
def notebook_loader():
    @contextmanager
    def notebook_helper(nb_path, prerun=None, **kwargs):
        with open(nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        client = TestbookNotebookClient(nb)
        with client.setup_kernel(**kwargs):
            if prerun is not None:
                client.execute_cell(prerun)

            yield client

    return notebook_helper


def notebook(nb_path, prerun=None, **kwargs):
    def wrapper(func):
        with open(nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        client = TestbookNotebookClient(nb)

        def inner(*args, **kwargs):
            with client.setup_kernel(**kwargs):
                if prerun is not None:
                    client.execute_cell(prerun)

                return func(client, *args, **kwargs)

        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__

        return inner

    return wrapper
