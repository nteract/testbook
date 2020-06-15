from nbformat import NotebookNode


class TestbookNode(NotebookNode):
    """
    Extends `NotebookNode` to perform assertions
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @property
    def output_text(self):
        text = ''
        for output in self['outputs']:
            if 'text' in output:
                text += output['text']

        return text.strip()
