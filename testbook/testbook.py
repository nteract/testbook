import functools
from unittest.mock import DEFAULT

import nbformat


from .client import TestbookNotebookClient


class testbook:
    """`testbook` acts as function decorator or a context manager.

    When the function/with statement exits the kernels started when
    entering the function/with statement will be terminated.

    If `testbook` is used as a decorator, the `TestbookNotebookClient`
    will be passed as first argument to the decorated function.
    """

    # Developer notes:
    #
    # To trick pytest, we mimic the API of unittest.mock.patch in testbook.
    # Notably, the following elements are added:
    # * attribute_name, Class attribute (see below)
    # * new, Instance attribute (see __init__)
    # * patchings, wrapper attributes (see __call__)

    attribute_name = None

    def __init__(
        self, nb, execute=None, timeout=60, kernel_name='python3', allow_errors=False, **kwargs
    ):
        self.execute = execute
        self.client = TestbookNotebookClient(
            nbformat.read(nb, as_version=4) if not isinstance(nb, nbformat.NotebookNode) else nb,
            timeout=timeout,
            allow_errors=allow_errors,
            kernel_name=kernel_name,
            **kwargs
        )

        self.new = DEFAULT

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
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # pragma: no cover
            with self.client.setup_kernel():
                self._prepare()
                return func(self.client, *args, **kwargs)

        wrapper.patchings = [self]
        return wrapper
