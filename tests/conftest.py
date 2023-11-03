import os
import tempfile

import pytest
from api import create_app 

@pytest.fixture(scope='package')
def app():
    # Creates and opens a temporary file, where db_fd is the file descriptor
    # and db_path is the path to it. This overrides the DATABASE path to the
    # temporary path instead of the instance folder
    db_fd, db_path = tempfile.mkstemp()

    # Creates the app in testing mode, using the temporary database 
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Initializes the app's database
    with app.app_context():
        from api.database import init_db
        init_db()

    yield app

    # Cleans up the temporary file creation
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='package')
def client(app):
    return app.test_client()

@pytest.fixture(scope='package')
def runner(app):
    return app.test_cli_runner()
    