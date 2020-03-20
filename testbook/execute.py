from functools import wraps

import nbformat

from testbook.client import TestbookNotebookClient


def execute_cell(notebook_filename, cell_index):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(notebook_filename) as f:
                nb = nbformat.read(f, as_version=4)

            client = TestbookNotebookClient(nb)
            nb_executed = client.testbook_execute_cell(
                cell=nb['cells'][cell_index], cell_index=cell_index
            )

            func(nb_executed['cells'][cell_index], *args, **kwargs)

        return wrapper

    return decorator
