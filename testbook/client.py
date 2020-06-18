import json
from collections.abc import Callable
from inspect import getsource
from textwrap import dedent

from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbformat.v4 import new_code_cell

from .exceptions import TestbookCellTagNotFoundError, TestbookError
from .testbooknode import TestbookNode


class TestbookNotebookClient(NotebookClient):
    def __init__(self, nb, km=None, **kw):
        super().__init__(nb, km=km, **kw)

    @property
    def cells(self):
        return self.nb.cells

    @staticmethod
    def _execute_result(outputs):
        """Return data from execute_result outputs"""

        if not outputs:
            return

        return [output["data"] for output in outputs if output.output_type == 'execute_result']

    def _cell_index(self, tag):
        """Get cell index from the cell tag"""

        if isinstance(tag, int):
            return tag
        elif not isinstance(tag, str):
            raise TypeError('expected tag as str')

        for idx, cell in enumerate(self.nb['cells']):
            metadata = cell['metadata']
            if "tags" in metadata and tag in metadata['tags']:
                return idx

        raise TestbookCellTagNotFoundError("Cell tag '{}' not found".format(tag))

    def execute_cell(self, cell, **kwargs):
        """Executes a cell or list of cells

        Parameters
        ----------
            cell : int or str or list
                cell index (or cell tag)

        Returns
        -------
            executed_cells : dict or list
        """

        if not isinstance(cell, list):
            cell = [cell]

        cell_indexes = cell

        if all(isinstance(x, str) for x in cell):
            cell_indexes = [self._cell_index(tag) for tag in cell]

        executed_cells = []
        for idx in cell_indexes:
            try:
                cell = super().execute_cell(self.nb['cells'][idx], idx, **kwargs)
            except CellExecutionError as e:
                raise TestbookError(str(e)) from None

            executed_cells.append(cell)

        return executed_cells[0] if len(executed_cells) == 1 else executed_cells

    def cell_output_text(self, cell):
        """Return cell text output

        Parameters
        ----------
            cell : int or str
                cell index (or cell tag)

        Returns
        -------
            text : str
        """

        cell_index = cell
        if isinstance(cell, str):
            cell_index = self._cell_index(cell)
        text = ''
        outputs = self.nb['cells'][cell_index]['outputs']
        for output in outputs:
            if 'text' in output:
                text += output['text']

        return text.strip()

    def inject(self, code, args=None, run=False, before=None, after=None):
        """Injects and executes given code block

        Parameters
        ----------
            code :  str or Callable
                Code or function to be injected
            args : tuple (optional)
                tuple of arguments to be passed to the function
            run : bool (optional)
                If True, the code is immediately executed after injection.
                Defaults to False.
            before : str or int (optional)
                Inject code before cell
            after : str or int (optional)
                Inject code after cell
        Returns
        -------
            cell : TestbookNode
        """

        if isinstance(code, str):
            lines = dedent(code)
        elif isinstance(code, Callable):
            lines = getsource(code) + dedent(
                """
                # Calling {func_name}
                {func_name}({args_str})
                """.format(
                    func_name=code.__name__,
                    args_str=', '.join(map(json.dumps, args)) if args else '',
                )
            )
        else:
            raise TypeError('can only inject function or code block as str')

        inject_idx = len(self.cells)

        if after is not None and before is not None:
            raise ValueError("pass either before or after as kwargs")
        elif before is not None:
            inject_idx = self._cell_index(before)
        elif after is not None:
            inject_idx = self._cell_index(after) + 1

        code_cell = new_code_cell(lines)
        self.cells.insert(inject_idx, code_cell)

        return TestbookNode(self.execute_cell(inject_idx)) if run else TestbookNode(code_cell)

    def value(self, name):
        """Extract a JSON-able variable value from notebook kernel"""

        result = self.inject(name, run=True)
        if not self._execute_result(result.outputs):
            raise TestbookError('code provided does not produce execute_result')

        code = """
        from IPython.display import JSON
        JSON({"value" : _})
        """
        cell = self.inject(code, run=True)
        return cell.outputs[0].data['application/json']['value']
