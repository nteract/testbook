from contextlib import contextmanager

import nbformat

from testbook.client import TestbookNotebookClient


class notebook_loader:
    def __init__(self, nb_path, prerun=None):
        self.nb_path = nb_path
        self.prerun = prerun

        with open(self.nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        self.client = TestbookNotebookClient(nb)

    def _start_kernel(self):
        if self.client.km is None:
            self.client.start_kernel_manager()

        if not self.client.km.has_kernel:
            self.client.start_new_kernel_client()

    def __enter__(self):
        self._start_kernel()
        if self.prerun is not None:
            self.client.execute_cell(self.prerun)
        return self.client

    def __exit__(self, *args):
        self.client._cleanup_kernel()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.client.setup_kernel():
                if self.prerun is not None:
                    self.client.execute_cell(self.prerun)
                func(self.client, *args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper
