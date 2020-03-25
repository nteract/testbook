from nbclient import NotebookClient
from nbclient.client import CellExecutionError


class TestbookNotebookClient(NotebookClient):
    def execute_cell(self, cell_index, execution_count=None, store_history=True):
        if not isinstance(cell_index, list):
            cell_index = [cell_index]
        executed_cells = []

        for idx in cell_index:
            cell = super().execute_cell(
                self.nb['cells'][idx],
                idx,
                execution_count=execution_count,
                store_history=store_history,
            )
            executed_cells.append(cell)

        return executed_cells

    def cell_output_text(self, cell_index):
        """Return cell text output
        
        Arguments:
            cell_index {int} -- cell index in notebook
        
        Returns:
            str -- Text output
        """

        text = ''
        outputs = self.nb['cells'][cell_index]['outputs']
        for output in outputs:
            if 'text' in output:
                text += output['text']

        return text

    def cell_output(self, cell_index):
        """Return cell text output
        
        Arguments:
            cell_index {int} -- cell index in notebook
        
        Returns:
            list -- List of outputs for the given cell
        """

        outputs = self.nb['cells'][cell_index]['outputs']
