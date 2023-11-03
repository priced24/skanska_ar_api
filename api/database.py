import json
import os

import click
import datetime
from flask import current_app
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


# Defines the path where test data is located
TEST_DATA_JSON_RELATIVE_PATH = 'api/test_data/test_data.json'
test_data_path = os.path.join(os.getcwd(), TEST_DATA_JSON_RELATIVE_PATH)

# NOTE: Might need to include convert_unicode=True parameter
# This converts all Unicode values to raw bytes and from raw byte values back to Python Unicode
engine = create_engine('sqlite:///' + current_app.config['DATABASE'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """ init_db

    Initializes the database's tables using the models defined in api.models
    """
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()
    from . import models
    Base.metadata.create_all(bind=engine)


def shutdown_session(exception=None):
    """ shutdown_session

    Removes the database session at the end of the request or
    when the application shutsdown
    """
    db_session.remove()


def bulk_create_from_json_list(json_list, model):
    """ bulk_create_from_json_list

    Helper function for bulk creating model instances from JSON.

    Parameters:
        json_list - list of JSON serialized objects of model instances
        model - the model the instances are of

    Returns:
        success - whether the instances were created successfully
        message - error message if creation fails
    """
    success = True
    message = ''
    try:
        db_session.execute(
            insert(model),
            json_list
        )
        db_session.commit()
    except IntegrityError as e:
        success = False
        message = e
    return success, message


@click.command('init_db')
@click.option('--dummy', '-d', is_flag=True, default=False, show_default=True,
              help='Initialize the databse with dummy data')
@click.option('--verbose', '-v', default=True, show_default=True,
              help='Whether status changes should be printed')
def init_db_command(dummy, verbose):
    """ init_db

    Initializes the database's tables using the models defined in `api.models`.
    and with dummy data contained in `api/test_data/test_data.json`.

    Parameters:
        dummy - whether the database should be initialized with dummy data
        verbose - whether initialization should print status changes to the terminal
    """
    # Clears the existing data and create new table
    init_db()
    if verbose:
        click.echo('Database Initialized.')

    if dummy:
        from .constants import URL_MODEL_MAPPING
        # Creates a mapping between model names and classes
        models = {cls.__name__: cls for cls in URL_MODEL_MAPPING.values()}

        if verbose:
            click.echo('Adding dummy data to database.')
        with open(TEST_DATA_JSON_RELATIVE_PATH, 'r') as json_file:
            data_json = json.load(json_file)

            for name, cls in models.items():
                if name in data_json:
                    # Convert date/time field into a datetime object for SensorDataReadable
                    if name == 'SensorDataReadable':
                        for i, entry in enumerate(data_json[name]):
                            format = '%Y-%m-%d %H:%M:%S'
                            dtime = entry['datetime']
                            dt_object = datetime.datetime.strptime(
                                dtime, format)
                            data_json[name][i]['datetime'] = dt_object

                    # Bulk creates records
                    success, message = bulk_create_from_json_list(
                        data_json[name], cls)
                    output = f'\t{name} records created successfully.'
                    if not success:
                        output = f'\tAn error occurred creating {name} records:\n{message}'
                    if verbose:
                        click.echo(output)

        if verbose:
            click.echo('Completed adding dummy data.')


def init_app(app):
    """ init_app

    Parameters:
        app - Flask app instance

    Initializes the app instance by registering the `shutdown_session` and
    `init_db_command` functions with the application context.
    """
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
