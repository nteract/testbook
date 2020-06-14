import json
from collections.abc import Callable
from inspect import getsource
from textwrap import dedent

from nbclient import NotebookClient
from nbformat.v4 import new_code_cell

from testbook.exceptions import CellTagNotFoundError
from testbook.testbooknode import TestbookNode


class TestbookNotebookClient(NotebookClient):
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

        raise CellTagNotFoundError("Cell tag '{}' not found".format(tag))

    def execute_cell(self, cell, **kwargs):
        """Executes a cell or list of cells

        Parameters
        ----------
            cell : int or str
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
            cell = super().execute_cell(self.nb['cells'][idx], idx, **kwargs)
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

    def inject(self, code, args=None, prerun=None):
        """Injects and executes given code block

        Parameters
        ----------
            code :  str or Callable
                Code or function to be injected
            args : tuple (optional)
                tuple of arguments to be passed to the function
            prerun : list (optional)
                list of cells to be pre-run prior to injection
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

        if prerun is not None:
            self.execute_cell(prerun)

        self.nb.cells.append(new_code_cell(lines))
        cell = self.execute_cell(len(self.nb.cells) - 1)

        return TestbookNode(cell)
