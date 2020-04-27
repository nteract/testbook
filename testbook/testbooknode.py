from nbformat import NotebookNode


class TestbookNode(NotebookNode):
    """
    Extends `NotebookNode` to perform assertions
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def assert_output_text(self, expected_text):
        text = ''
        for output in self['outputs']:
            if 'text' in output:
                text += output['text']

        assert text.strip() == expected_text.strip()
