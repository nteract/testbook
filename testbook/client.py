import inspect
import json
import textwrap
from collections.abc import Callable

from nbformat.v4 import new_code_cell

from nbclient import NotebookClient
from testbook.testbooknode import TestbookNode


class TestbookNotebookClient(NotebookClient):
    def _get_cell_index(self, tag):
        """Get cell index from the cell tag

        Arguments:
            nb {dict} -- Notebook
            tag {str} -- tag

        Returns:
            int -- cell index
        """
        if isinstance(tag, int):
            return tag
        elif not isinstance(tag, str):
            raise TypeError('expected tag as str')

        for idx, cell in enumerate(self.nb['cells']):
            metadata = cell['metadata']
            if "tags" in metadata and tag in metadata['tags']:
                return idx

    def execute_cell(self, cell, execution_count=None, store_history=True):
        if not isinstance(cell, list):
            cell = [cell]

        cell_indexes = cell

        if all(isinstance(x, str) for x in cell):
            cell_indexes = [self._get_cell_index(tag) for tag in cell]

        executed_cells = []
        for idx in cell_indexes:
            cell = super().execute_cell(
                self.nb['cells'][idx],
                idx,
                execution_count=execution_count,
                store_history=store_history,
            )
            executed_cells.append(cell)

        return executed_cells[0] if len(executed_cells) == 1 else executed_cells

    def cell_output_text(self, cell):
        """Return cell text output

        Arguments:
            cell {int} -- cell index in notebook

        Returns:
            str -- Text output
        """
        cell_index = cell
        if isinstance(cell, str):
            # Get cell index of this tag
            cell_index = self._get_cell_index(cell)
        text = ''
        outputs = self.nb['cells'][cell_index]['outputs']
        for output in outputs:
            if 'text' in output:
                text += output['text']

        return text

    def inject(self, func, args=None, prerun=None, **kwargs):
        """Injects given function and executes with arguments passed

        Arguments:
            func {__func__} -- function name
            args {list} -- list of arguments to be passed

        Returns:
            TestbookNode -- dict containing function and function call along with outputs
        """
        if isinstance(func, str):
            lines = textwrap.dedent(func)
        elif isinstance(func, Callable):
            lines = inspect.getsource(func)
            args_str = ', '.join(map(json.dumps, args)) if args else ''

            # Add the function call to the same cell
            lines += textwrap.dedent(
                f"""
                # Calling {func.__name__}
                {func.__name__}({args_str})
            """
            )
        else:
            raise TypeError('can only inject function or code block as str')

        # Execute the pre-run cells if passed
        if prerun or prerun == 0:
            self.execute_cell(prerun)

        # Create a code cell
        inject_cell = new_code_cell(lines)

        # Find where to inject the cell
        position = len(self.nb.cells)
        if "before" in kwargs:
            position = self._get_cell_index(kwargs["before"]) - 1
        elif "after" in kwargs:
            position = self._get_cell_index(kwargs["after"]) + 1

        # Insert it into the in memory notebook object and execute it
        self.nb.cells.insert(position, inject_cell)
        cell = self.execute_cell(position)

        return TestbookNode(cell)
