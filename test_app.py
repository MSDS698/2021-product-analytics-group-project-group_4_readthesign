from app import app

def test_app():
    """
    test availability of app
    """
    assert app is not None
