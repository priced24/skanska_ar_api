

def test_index(client):
    """ test_index
    
    Tests making a GET request to the root URL and that index.html is returned.
    """
    response = client.get('/')
    assert b'<title>AR Innovation Webapp</title>' in response.data
