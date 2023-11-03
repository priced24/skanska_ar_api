# Based on the following tutorial:
# https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/

import os
from flask_cors import CORS
from flask import Flask


def create_app(test_config=None):
    """
    create_app

    Application factory function that creates and returns an instance of the Flask app.
    """
    # Create and configure the Flask instance.
    # __name__ is used as the apps location and instance_relative_config specifies
    # that configuration files are relative to the instance folder located outside the
    # current directory.
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    # Sets default configurations that the app will use.
    app.config.from_mapping(
        SECRET_KEY='dev',  # Used for data safety -- should be overridden for production deployment
        # Path to the saved SQLite database file
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    if not test_config:
        # Load the instance config, if it exists, when not testing.
        # This should be used to set a SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exits (instance directory doesn't exist automatically)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # NOTE: This may be bad practice -- might revist later or
    # if issues start arising
    with app.app_context():
        from . import database
        database.init_app(app)

    # Depending on which decision we make for defining endpoints,
    # this registration will likely change.
    from api.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from api.views import bp as views_bp
    app.register_blueprint(views_bp)

    return app
