from testbook import testbook

@testbook('./dataframe-assertion-example.ipynb')
def test_dataframe_manipulation(tb):
    tb.execute_cell('imports')

    # Inject a dataframe with code
    tb.inject(
        """
        df = pd.DataFrame([[1, None, 3], [4, 5, 6]], columns=['a', 'b', 'c'], dtype='float')
        """
    )

    # Perform manipulation
    tb.execute_cell('manipulation')

    # Inject assertion into notebook
    tb.inject("assert len(df) == 1")
