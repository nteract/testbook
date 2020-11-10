from typing import List, Optional

import pytest
from jupyter_client import kernelspec
from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_notebook, new_code_cell, new_output


@pytest.fixture
def notebook_factory():
    """Pytest fixture to generate a valid notebook."""

    def notebook_generator(cells: Optional[List[NotebookNode]] = None) -> NotebookNode:
        """Generate an executable notebook.

        The notebook cells are the one passed as arguments or the hard-coded cells
        if no cells is provided.
        """
        metadata = {}
        for name in kernelspec.find_kernel_specs():
            ks = kernelspec.get_kernel_spec(name)
            metadata = {
                'kernelspec': {
                    'name': name,
                    'language': ks.language,
                    'display_name': ks.display_name,
                }
            }
            break

        if cells is not None:
            all_cells = cells
        else:  # Default cells
            all_cells = [
                new_code_cell('a = 2', metadata={"tags": []}),
                new_code_cell('b=22\nb', metadata={"tags": ["test"]}),
                new_code_cell(
                    "",
                    metadata={"tags": ["dummy-outputs"]},
                    outputs=[new_output('execute_result', data={"text/plain": "text"})],
                ),
            ]

        return new_notebook(metadata=metadata, cells=all_cells)

    return notebook_generator
