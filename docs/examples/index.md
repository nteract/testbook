# Examples

Here are some common testing patterns where testbook can help.

## Mocking requests library

**Notebook:**

![mock-requests-library](https://imgur.com/GM1YExq.png)

**Test:**

```python
from testbook import testbook

@testbook('/path/to/notebook.ipynb', execute=True)
def test_get_details(tb):
    with tb.patch('requests.get') as mock_get:
        get_details = tb.ref('get_details') # get reference to function
        get_details('https://my-api.com')

        mock_get.assert_called_with('https://my-api.com')
```

## Asserting dataframe manipulations

**Notebook:**

![dataframe-manip](https://imgur.com/g1DrVn2.png)

**Test:**

```python
from testbook import testbook

@testbook('/path/to/notebook.ipynb')
def test_dataframe_manipulation(tb):
    tb.execute_cell('imports')

    # Inject a dataframe with code
    tb.inject(
        """
        df = pandas.DataFrame([[1, None, 3], [4, 5, 6]], columns=['a', 'b', 'c'], dtype='float')
        """
    )

    # Perform manipulation
    tb.execute_cell('manipulation')

    # Inject assertion into notebook
    tb.inject("assert len(df) == 1")
```

## Asserting STDOUT of a cell

**Notebook:**

![dataframe-manip](https://imgur.com/cgtvkph.png)

**Test:**

```python
from testbook import testbook

@testbook('stdout.ipynb', execute=True)
def test_stdout(tb):
    assert tb.cell_output_text(1) == 'hello world!'

    assert 'The current time is' in tb.cell_output_text(2)
```
