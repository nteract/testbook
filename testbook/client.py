from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


class TestbookNotebookClient(NotebookClient):
    """
    Module containing a  that executes the code cells
    and updates outputs
    """

    def __init__(self, nb, km=None, **kw):
        """Initializes the execution manager.
        Parameters
        ----------
        nb : Notebook
        km : KernerlManager (optional)
            Optional kernel manager. If none is provided, a kernel manager will
            be created.
        """
        super().__init__(nb, km=km, **kw)

    def execute(self, **kwargs):
        """
        Wraps the parent class process call slightly
        """
        self.reset_execution_trackers()

        with self.setup_kernel(**kwargs):
            self.log.info("Executing notebook with kernel: %s" % self.kernel_name)
            self.testbook_execute_cells()
            info_msg = self._wait_for_reply(self.kc.kernel_info())
            self.nb.metadata['language_info'] = info_msg['content']['language_info']
            self.set_widgets_metadata()

        return self.nb

    def testbook_execute_cell(
        self, cell, cell_index, execution_count=None, store_history=True, **kwargs
    ):
        """
        Wraps the parent class process call slightly
        """
        self.reset_execution_trackers()

        with self.setup_kernel(**kwargs):
            self.log.info("Executing notebook with kernel: %s" % self.kernel_name)
            self.execute_cell(cell, cell_index, execution_count, store_history)
            info_msg = self._wait_for_reply(self.kc.kernel_info())
            self.nb.metadata['language_info'] = info_msg['content']['language_info']
            self.set_widgets_metadata()

        return self.nb

