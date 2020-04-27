from testbook import notebook_loader


def test_execute_cell():
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.execute_cell(1)
        assert notebook.cell_output_text(1) == 'hello world\n[1, 2, 3]\n'

        notebook.execute_cell([2, 3])
        assert notebook.cell_output_text(3) == 'foo\n'


def test_execute_cell_tags():
    with notebook_loader('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.execute_cell('test1')
        assert notebook.cell_output_text('test1') == 'hello world\n[1, 2, 3]\n'

        notebook.execute_cell(['prepare_foo', 'execute_foo'])
        assert notebook.cell_output_text('execute_foo') == 'foo\n'


@notebook_loader("testbook/tests/resources/foo.ipynb")
def test_notebook(notebook):
    notebook.execute_cell('test1')
    assert notebook.cell_output_text('test1') == 'hello world\n[1, 2, 3]\n'

    notebook.execute_cell(['prepare_foo', 'execute_foo'])
    assert notebook.cell_output_text('execute_foo') == 'foo\n'


@notebook_loader("testbook/tests/resources/foo.ipynb", prerun='test1')
def test_notebook_with_prerun(notebook):
    assert notebook.cell_output_text(1) == 'hello world\n[1, 2, 3]\n'
