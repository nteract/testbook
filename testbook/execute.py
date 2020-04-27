from contextlib import contextmanager

import nbformat
import pytest

from testbook.client import TestbookNotebookClient


class notebook_loader:
    def __init__(self, nb_path, prerun=None):
        self.nb_path = nb_path
        self.prerun = prerun

        with open(self.nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        client = TestbookNotebookClient(nb)

        if self.prerun is not None:
            with client.setup_kernel():
                client.execute_cell(self.prerun)

        self.client = client

    def _start_kernel(self):
        if self.client.km is None:
            self.client.start_kernel_manager()

        if not self.client.km.has_kernel:
            self.client.start_new_kernel_client()

    def __enter__(self):
        self._start_kernel()
        return self.client

    def __exit__(self, *args):
        self.client._cleanup_kernel()

    def __call__(self, func):
        def wrapper():
            self._start_kernel()

            def inner(*args, **kwargs):
                return func(self.client, *args, **kwargs)

            self.client._cleanup_kernel()

            inner.__name__ = func.__name__
            inner.__doc__ = func.__doc__

            return inner

        return wrapper
