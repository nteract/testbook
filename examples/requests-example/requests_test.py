from testbook import testbook

@testbook('./requests-test.ipynb', execute=True)
def test_get_details(tb):
    with tb.patch('requests.get') as mock_get:
        get_details = tb.ref('get_details') # get reference to function
        get_details('https://my-api.com')

        mock_get.assert_called_with('https://my-api.com')
