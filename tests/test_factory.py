from api import create_app


def test_config():
    """ test_config
    
    Tests if the app is configured to TESTING when instantiated.
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
