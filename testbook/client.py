from contextlib import contextmanager
from inspect import getsource
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union

from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbformat.v4 import new_code_cell

from .exceptions import (
    TestbookCellTagNotFoundError,
    TestbookExecuteResultNotFoundError,
    TestbookSerializeError,
    TestbookRuntimeError,
    TestbookError,
)
from .reference import TestbookObjectReference
from .testbooknode import TestbookNode
from .translators import PythonTranslator
from .utils import random_varname, all_subclasses


class TestbookNotebookClient(NotebookClient):
    def __init__(self, nb, km=None, **kw):
        super().__init__(nb, km=km, **kw)

    def ref(self, name: str) -> TestbookObjectReference:
        """
        Return a reference to an object in the kernel
        """

        # Check if exists
        self.inject(name, pop=True)
        return TestbookObjectReference(self, name)

    @staticmethod
    def _construct_call_code(
        func_name: str, args: Optional[List] = None, kwargs: Optional[Dict] = None
    ) -> str:
        return """
            {func_name}(*{args_list}, **{kwargs_dict})
            """.format(
            func_name=func_name,
            args_list=PythonTranslator.translate(args) if args else [],
            kwargs_dict=PythonTranslator.translate(kwargs) if kwargs else {},
        )

    @property
    def cells(self):
        return self.nb.cells

    @staticmethod
    def _execute_result(cell) -> List:
        """
        Return data from execute_result outputs
        """

        return [
            output["data"]
            for output in cell["outputs"]
            if output["output_type"] == 'execute_result'
        ]

    @staticmethod
    def _output_text(cell) -> str:
        if "outputs" not in cell:
            raise ValueError("cell must be a code cell")

        text = ''
        for output in cell["outputs"]:
            if 'text' in output:
                text += output['text']

        return text.strip()

    def _cell_index(self, tag: Union[int, str]) -> int:
        """
        Get cell index from the cell tag
        """

        if isinstance(tag, int):
            return tag
        elif not isinstance(tag, str):
            raise TypeError('expected tag as str')

        for idx, cell in enumerate(self.cells):
            metadata = cell['metadata']
            if "tags" in metadata and tag in metadata['tags']:
                return idx

        raise TestbookCellTagNotFoundError("Cell tag '{}' not found".format(tag))

    def execute_cell(self, cell, **kwargs) -> Union[Dict, List[Dict]]:
        """
        Executes a cell or list of cells
        """
        if isinstance(cell, slice):
            start, stop = self._cell_index(cell.start), self._cell_index(cell.stop)
            if cell.step is not None:
                raise TestbookError('testbook does not support step argument')

            cell = range(start, stop + 1)
        elif isinstance(cell, str) or isinstance(cell, int):
            cell = [cell]

        cell_indexes = cell

        if all(isinstance(x, str) for x in cell):
            cell_indexes = [self._cell_index(tag) for tag in cell]

        executed_cells = []
        for idx in cell_indexes:
            try:
                cell = super().execute_cell(self.nb['cells'][idx], idx, **kwargs)
            except CellExecutionError as ce:
                # Look for in-built Python exception
                eclass = None
                for klass in all_subclasses(Exception):
                    if klass.__name__ == ce.ename:
                        eclass = klass
                        break

                raise TestbookRuntimeError(ce.evalue, ce, eclass)

            executed_cells.append(cell)

        return executed_cells[0] if len(executed_cells) == 1 else executed_cells

    def execute(self) -> None:
        """
        Executes all cells
        """

        for index, cell in enumerate(self.nb.cells):
            super().execute_cell(cell, index)

    def cell_output_text(self, cell) -> str:
        """
        Return cell text output
        """

        cell_index = cell
        if isinstance(cell, str):
            cell_index = self._cell_index(cell)

        return self._output_text(self.nb['cells'][cell_index])

    def inject(
        self,
        code: str,
        args: List = None,
        kwargs: Dict = None,
        run: bool = True,
        before: Optional[Union[str, int]] = None,
        after: Optional[Union[str, int]] = None,
        pop: bool = False,
    ) -> TestbookNode:
        """Injects and executes given code block

        Parameters
        ----------
        code : str
            Code or function to be injected
        args : iterable, optional
            tuple of arguments to be passed to the function
        kwargs : dict, optional
            dict of keyword arguments to be passed to the function
        run : bool, optional
            Control immediate execution after injection (default is True)
        before, after : int, str, optional
            Inject code before or after cell
        pop : bool
            Pop cell after execution (default is False)

        Returns
        -------
        TestbookNode
            Injected cell
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

    def value(self, code: str) -> Any:
        """
        Execute given code in the kernel and return JSON serializeable result.

        If the result is not JSON serializeable, it raises `TestbookAttributeError`.
        This error object will also contain an attribute called `save_varname` which
        can be used to create a reference object with :meth:`ref`.

        Parameters
        ----------
        code: str
            This can be any executable code that returns a value.
            It can be used the return the value of an object, or the output
            of a function call.

        Returns
        -------
        The output of the executed code

        Raises
        ------
            TestbookSerializeError

        """
        result = self.inject(code, pop=True)

        if not self._execute_result(result):
            raise TestbookExecuteResultNotFoundError(
                'code provided does not produce execute_result'
            )

        save_varname = random_varname()

        inject_code = f"""
            {save_varname} = _

            import json
            json.dumps(_)

            from IPython.display import JSON
            JSON({{"value" : _}})
        """

        try:
            outputs = self.inject(inject_code, pop=True).outputs

            if outputs[0].output_type == "error":
                # will receive error when `allow_errors` is set to True
                raise TestbookRuntimeError(
                    outputs[0].evalue, outputs[0].traceback, outputs[0].ename
                )

            return outputs[0].data['application/json']['value']

        except TestbookRuntimeError:
            e = TestbookSerializeError('could not JSON serialize output')
            e.save_varname = save_varname
            raise e

    def _eq_in_notebook(self, lhs: str, rhs: Any) -> bool:
        return self.value("{lhs} == {rhs}".format(lhs=lhs, rhs=PythonTranslator.translate(rhs)))

    @contextmanager
    def patch(self, target, **kwargs):
        """Used as contextmanager to patch objects in the kernel"""
        mock_object = f'_mock_{random_varname()}'
        patcher = f'_patcher_{random_varname()}'

        self.inject(
            f"""
            from unittest.mock import patch
            {patcher} = patch(
                {PythonTranslator.translate(target)},
                **{PythonTranslator.translate(kwargs)}
            )
            {mock_object} = {patcher}.start()
        """
        )

        yield TestbookObjectReference(self, mock_object)

        self.inject(f"{patcher}.stop()")

    @contextmanager
    def patch_dict(self, in_dict, values=(), clear=False, **kwargs):
        """Used as contextmanager to patch dictionaries in the kernel"""
        mock_object = f'_mock_{random_varname()}'
        patcher = f'_patcher_{random_varname()}'

        self.inject(
            f"""
            from unittest.mock import patch
            {patcher} = patch.dict(
                {PythonTranslator.translate(in_dict)},
                {PythonTranslator.translate(values)},
                {PythonTranslator.translate(clear)},
                **{PythonTranslator.translate(kwargs)}
            )
            {mock_object} = {patcher}.start()
        """
        )

        yield TestbookObjectReference(self, mock_object)

        self.inject(f"{patcher}.stop()")
