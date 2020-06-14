from testbook import testbook


def test_execute_cell():
    with testbook('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.execute_cell(1)
        assert notebook.cell_output_text(1) == 'hello world\n[1, 2, 3]'

        notebook.execute_cell([2, 3])
        assert notebook.cell_output_text(3) == 'foo'


def test_execute_cell_tags():
    with testbook('testbook/tests/resources/foo.ipynb') as notebook:
        notebook.execute_cell('test1')
        assert notebook.cell_output_text('test1') == 'hello world\n[1, 2, 3]'

        notebook.execute_cell(['prepare_foo', 'execute_foo'])
        assert notebook.cell_output_text('execute_foo') == 'foo'


@testbook("testbook/tests/resources/foo.ipynb")
def test_testbook(notebook):
    notebook.execute_cell('test1')
    assert notebook.cell_output_text('test1') == 'hello world\n[1, 2, 3]'

    notebook.execute_cell(['prepare_foo', 'execute_foo'])
    assert notebook.cell_output_text('execute_foo') == 'foo'


@testbook("testbook/tests/resources/foo.ipynb", prerun='prepare_foo')
def test_testbook_with_prerun(notebook):
    notebook.execute_cell('execute_foo')
    assert notebook.cell_output_text('execute_foo') == 'foo'


def test_testbook_with_prerun_context_manager():
    with testbook("testbook/tests/resources/foo.ipynb", prerun='prepare_foo') as notebook:
        notebook.execute_cell('execute_foo')
        assert notebook.cell_output_text('execute_foo') == 'foo'
