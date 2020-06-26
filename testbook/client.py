from inspect import getsource
from textwrap import dedent

from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbformat.v4 import new_code_cell

from .exceptions import (
    TestbookCellTagNotFoundError,
    TestbookSerializeError,
    TestbookExecuteResultNotFoundError,
)
from .utils import random_varname
from .testbooknode import TestbookNode
from .translators import PythonTranslator
from .reference import TestbookObjectReference


class TestbookNotebookClient(NotebookClient):
    def __init__(self, nb, km=None, **kw):
        super().__init__(nb, km=km, **kw)

    def ref(self, name):
        # Check if exists
        self.inject(name)
        return TestbookObjectReference(self, name)

    @staticmethod
    def _construct_call_code(func_name, args=None, kwargs=None):
        return """
            {func_name}(*{args_list}, **{kwargs_dict})
            """.format(
            func_name=func_name,
            args_list=PythonTranslator.translate(args) if args else [],
            kwargs_dict=PythonTranslator.translate(args) if kwargs else {},
        )

    @property
    def cells(self):
        return self.nb.cells

    @staticmethod
    def _execute_result(cell):
        """Return data from execute_result outputs"""
        return [
            output["data"]
            for output in cell["outputs"]
            if output["output_type"] == 'execute_result'
        ]

    @staticmethod
    def _output_text(cell):
        if not cell["outputs"]:
            return
        text = ''
        for output in cell["outputs"]:
            if 'text' in output:
                text += output['text']

        return text.strip()

    def _cell_index(self, tag):
        """Get cell index from the cell tag"""

        if isinstance(tag, int):
            return tag
        elif not isinstance(tag, str):
            raise TypeError('expected tag as str')

        for idx, cell in enumerate(self.cells):
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
                # TODO: drop usage of eval
                raise eval(e.ename)(e) from None
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

        return self._output_text(self.nb['cells'][cell_index])

    def inject(self, code, args=None, kwargs=None, run=True, before=None, after=None, pop=False):
        """Injects and executes given code block

        Parameters
        ----------
            code :  str or callable
                Code or function to be injected
            args : tuple (optional)
                tuple of arguments to be passed to the function
            kwargs : dict (optional)
                dict of keyword arguments to be passed to the function
            run : bool (optional)
                If True, the code is immediately executed after injection.
                Defaults to False.
            before : str or int (optional)
                Inject code before cell
            after : str or int (optional)
                Inject code after cell
            pop : bool (optional)
                Pop cell after execution
        Returns
        -------
            cell : TestbookNode
        """

        if isinstance(code, str):
            lines = dedent(code)
        elif callable(code):
            lines = getsource(code) + (
                dedent(self._construct_call_code(code.__name__, args, kwargs)) if run else ''
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

        cell = TestbookNode(self.execute_cell(inject_idx)) if run else TestbookNode(code_cell)

        if run and pop:
            self.cells.pop(inject_idx)

        return cell

    def value(self, code, safe=False):
        result = self.inject(code, pop=True)

        if not self._execute_result(result):
            raise TestbookExecuteResultNotFoundError(
                'code provided does not produce execute_result'
            )

        save_varname = random_varname()

        inject_code = f"""
            {save_varname} = _

            from IPython.display import JSON
            JSON({{"value" : _}})
        """

        try:
            outputs = self.inject(inject_code, pop=True).outputs
            return outputs[0].data['application/json']['value']

        except ValueError:
            if not safe:
                raise TestbookSerializeError('could not JSON serialize output')

            return TestbookObjectReference(self, save_varname)

    def _eq_in_notebook(self, lhs, rhs):
        return self.value("{lhs} == {rhs}".format(lhs=lhs, rhs=PythonTranslator.translate(rhs)))
