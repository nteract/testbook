import nbformat

from .client import TestbookNotebookClient


class testbook:
    def __init__(self, nb, execute=None, timeout=60, allow_errors=False):
        self.execute = execute
        self.client = TestbookNotebookClient(
            nbformat.read(nb, as_version=4), timeout=timeout, allow_errors=allow_errors
        )

    def _prepare(self):
        if self.execute is True:
            self.client.execute()
        elif self.execute not in [None, False]:
            self.client.execute_cell(self.execute)

    def __enter__(self):
        with self.client.setup_kernel(cleanup_kc=False):
            self._prepare()
            return self.client

    def __exit__(self, *args):
        self.client._cleanup_kernel()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.client.setup_kernel():
                self._prepare()
                func(self.client, *args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper
