from testbook import testbook

@testbook('stdout-assertion-example.ipynb', execute=True)
def test_stdout(tb):
    assert tb.cell_output_text(1) == 'hello world!'

    assert 'The current time is' in tb.cell_output_text(2)
