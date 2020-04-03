from contextlib import contextmanager

import nbformat
import pytest

from testbook.client import TestbookNotebookClient


@pytest.fixture
def notebook_loader():
    @contextmanager
    def notebook_helper(nb_path, **kwargs):
        with open(nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        client = TestbookNotebookClient(nb)
        with client.setup_kernel(**kwargs):
            yield client

    return notebook_helper
