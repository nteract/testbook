import inspect
import json
import textwrap
from collections.abc import Callable

from nbformat.v4 import new_code_cell

from nbclient import NotebookClient
from nbclient.client import CellExecutionError
from testbook.testbooknode import TestbookNode
from testbook.utils import get_cell_index


class TestbookNotebookClient(NotebookClient):
    def execute_cell(self, cell, execution_count=None, store_history=True):
        if not isinstance(cell, list):
            cell = [cell]

        cell_idx = cell

        if all(isinstance(x, str) for x in cell):
            cell_idx = [get_cell_index(self.nb, tag) for tag in cell]

        executed_cells = []

        for idx in cell_idx:
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
            cell_index = get_cell_index(self.nb, cell)
        text = ''
        outputs = self.nb['cells'][cell_index]['outputs']
        for output in outputs:
            if 'text' in output:
                text += output['text']

        return text

    def inject(self, func, args=None):
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

        # Create a code cell
        inject_cell = new_code_cell(lines)

        # Insert it into the in memory notebook object and execute it
        self.nb.cells.append(inject_cell)
        cell = self.execute_cell(len(self.nb.cells) - 1)

        return TestbookNode(cell)
