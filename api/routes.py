import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from .database import db_session
from .constants import StatusCode, URL_MODEL_MAPPING, DATETIME_FORMAT_STRING
from .models import Building, Room, Sensor, SensorDataReadable
from .validators import generate_validator, get_request_validator

# Views and other code can be registered to the blueprint, rather than
# the application directly.
bp = Blueprint('api', __name__, url_prefix='/')


class InvalidAPIUsage(Exception):
    """ InvalidAPIUsage

    Custom exception class for defining descriptive error messages.
    Based on the following:
    https://flask.palletsprojects.com/en/2.2.x/errorhandling/#returning-api-errors-as-json
    """
    status_code = StatusCode.BAD_REQUEST.value  # Bad request

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()

        self.message = message
        # Updates excpetion status code if present
        if status_code:
            self.status_code = status_code.value
        self.payload = payload

    def to_dict(self):
        """ to_dict

        Returns a dictionary representation of the exception
        """
        dict_repr = dict(self.payload or ())
        dict_repr['message'] = self.message
        return dict_repr


class IndexAPI(MethodView):
    """ IndexAPI

    Implements generic API request handling for a single entry of a given model.

    Dispatches request methods to the corresponding instance methods,
    i.e. GET requests are handled by the `get` method.

    GET and DELETE are the only two HTTP request types that are implemented.
    Other request types can be implemented as we see fit.
    """
    init_every_request = False

    def __init__(self, model):
        self.model = model
        # Add validator function
        # self.validator = generate_validator(model)

    def _get_record(self, id):
        """ _get_record

        Private helper function for querying a record. 
        If a record doesn't exist for the given id, a exception is raised.

        Parameters:
            id - id corresponding to a model record
        Returns:
            model record        
        """
        model_record = self.model.query.filter(self.model.id == id).first()
        if not model_record:
            raise InvalidAPIUsage(
                f'No {str(self.model)} record exist for id: {id}',
                status_code=StatusCode.NOT_FOUND
            )

        return model_record

    def get(self, id):
        """ get

        Handles GET requests 

        Parameters:
            id - id corresponding to a model record
        Returns:
            JSON Response of the record
        """

        record = self._get_record(id)
        return jsonify(record.to_json())

    def delete(self, id):
        """ delete

        Handle DELETE requestss

        Parameters:
            id - id corresponding to a model record
        Returns:
            empty string with a 204 - No Content status code
        """
        record = self._get_record(id)
        db_session.delete(record)
        db_session.commit()

        return '', StatusCode.NO_CONTENT.value


class ListAPI(MethodView):
    """ ListAPI

    Implements generic API request handling for multiple entries of a given model.

    Dispatches request methods to the corresponding instance methods,
    i.e. GET requests are handled by the `get` method.

    GET and POST are the only two HTTP request types that are implemented.
    Other request types can be implemented as we see fit.
    """
    init_every_request = False

    def __init__(self, model):
        self.model = model
        # Uses the model to generate a validator function for POST requests
        self.validate = generate_validator(model)

    def _query_from_building(self, datetime_from, datetime_to):
        """ _query_from_building

        Helper function for querying sensor data within a specified datatime
        range for a given building.

        Parameters:
            datetime_from - datetime object representing the time 'from'
            datetime_to - datatime object representing the time 'to'

        Returns:
            the result of the query
        """
        return (self.model.query
                .join(Room, Room.building_id == Building.id)
                .join(Sensor, Sensor.room_id == Room.id)
                .join(SensorDataReadable, SensorDataReadable.sensor_id == Sensor.id)
                .filter(
                    datetime_from <= SensorDataReadable.datetime,
                    datetime_to >= SensorDataReadable.datetime
                ).all())

    def _query_from_room(self, datetime_from, datetime_to):
        """ _query_from_room

        Helper function for querying sensor data within a specified datatime
        range from a given room.

        Parameters:
            datetime_from - datetime object representing the time 'from'
            datetime_to - datatime object representing the time 'to'

        Returns:
            the result of the query
        """
        return (self.model.query
                .join(Sensor, Sensor.room_id == Room.id)
                .join(SensorDataReadable, SensorDataReadable.sensor_id == Sensor.id)
                .filter(
                    datetime_from <= SensorDataReadable.datetime,
                    datetime_to >= SensorDataReadable.datetime
                ).all())

    def _query_from_sensor(self, datetime_from, datetime_to):
        """ _query_from_sensor

        Helper function for querying sensor data within a specified datatime
        range from a given sensor.

        Parameters:
            datetime_from - datetime object representing the time 'from'
            datetime_to - datatime object representing the time 'to'

        Returns:
            the result of the query
        """
        return (self.model.query
                .join(SensorDataReadable, SensorDataReadable.sensor_id == Sensor.id)
                .filter(
                    datetime_from <= SensorDataReadable.datetime,
                    datetime_to >= SensorDataReadable.datetime
                ).all())

    def _query_sensor_data(self, datetime_from, datetime_to):
        """ _query_sensor_data

        Helper function for querying sensor data with a sepcified datatime range.

        Parameters:
            datetime_from - datetime object representing the time 'from'
            datetime_to - datetime object representing the time 'to'

        Returns:
            the result of the query
        """
        return (self.model.query.filter(
                datetime_from <= SensorDataReadable.datetime,
                datetime_to >= SensorDataReadable.datetime
                ).all())

    def _get_record_from_t(self, datetime_from, datetime_to):
        """ _get_record

        Private helper function for querying a record from a time. 
        If a record doesn't exist between the given date ranges , a exception is raised.

        Parameters:
            datetime_from - corresponds to the time frame that we are starting the query 
            datetime_to - corresponds to the time frame that we are ending the query
        Returns:
            model record        
        """
        switch = {
            Building: self._query_from_building,
            Room: self._query_from_room,
            Sensor: self._query_from_sensor,
            SensorDataReadable: self._query_sensor_data
        }

        # Selects the query function based on the model
        query = switch.get(self.model, None)
        if not query:
            return []

        return query(datetime_from, datetime_to)

    def get(self):
        """ get

        Handles GET requests 

        Returns:
            JSON Response of all available records
        """
        if request.is_json:
            body_json = request.json
            is_valid = get_request_validator(request.json)
            if not is_valid:
                raise InvalidAPIUsage(
                    'Invalid raw body structure for request.'
                )

            datetime_from = body_json.get('dateTimeFrom', None)
            datetime_to = body_json.get('dateTimeTo', None)

            if datetime_from and datetime_to:
                datetime_from = datetime.datetime.strptime(
                    datetime_from, DATETIME_FORMAT_STRING)
                datetime_to = datetime.datetime.strptime(
                    datetime_to, DATETIME_FORMAT_STRING)
                records = self._get_record_from_t(datetime_from, datetime_to)
            else:
                records = self.model.query.all()
        else:
            records = self.model.query.all()

        return jsonify([record.to_json() for record in records])

    def _create_record(self, **kwargs):
        """ _create_record

        Private helper function for creating a record. It's assumed that
        arguments passed in are valid JSON for the given model.

        Parameters:
            **kwargs - key/value fields for creating a record
        Returns:
            Newly created model record
        """
        new_record = self.model(**kwargs)
        return new_record

    def post(self):
        """ post

        Handles POST requests

        Returns:
            JSON Response of the newly created record.
        """

        json_body = request.json

        is_valid = self.validate(json_body)
        if not is_valid:
            raise InvalidAPIUsage(
                'Invalid raw body structure for request.'
            )

        new_record = self._create_record(**json_body)
        # Create Building object using fields given in Post JSON
        if self.model == Building:
            db_session.add(new_record)

        # Create Room object and assign it to the appropriate Building if it exsists
        elif self.model == Room:
            building_id = json_body.pop('building_id')
            building = db_session.get(Building, building_id)
            if not building:
                raise InvalidAPIUsage(
                    f'No building record exist for id: {building_id}',
                    status_code=StatusCode.NOT_FOUND
                )
            new_record.building = building
            db_session.add(new_record)

        # Create Sensor object and assign it to the appropriate Room if it exsists
        elif self.model == Sensor:
            room_id = json_body.pop('room_id')
            room = db_session.get(Room, room_id)
            if not room:
                raise InvalidAPIUsage(
                    f'No room record exist for id: {room_id}',
                    status_code=StatusCode.NOT_FOUND
                )
            new_record.room = room
            db_session.add(new_record)

        elif self.model == SensorDataReadable:
            sensor_id = json_body.pop('sensor_id')
            dtime = json_body['datetime']
            dt = datetime.datetime.strptime(dtime, DATETIME_FORMAT_STRING)
            sensor = db_session.get(Sensor, sensor_id)
            if not sensor:
                raise InvalidAPIUsage(
                    f'No room record exist for id: {sensor_id}',
                    status_code=StatusCode.NOT_FOUND
                )
            new_record.sensor = sensor
            new_record.datetime = dt
            db_session.add(new_record)

        db_session.commit()
        return jsonify(new_record.to_json())


@bp.errorhandler(InvalidAPIUsage)
def invalid_api_usage(exception):
    """
    invalid_api_usage

    Application function handler for InvalidAPIUsage exceptions.

    Parameter:
        exception - instance of InvalidAPIUsage

    Returns:
        JSON response of the exception 
    """
    return jsonify(exception.to_dict()), exception.status_code


def register_api_for_model(bp, model, name):
    """ register_api_for_model

    Initializes Index and List APIs for the given model, and registers
    them with the provided Blueprint, `bp`.

    Parameters:
        bp - Blueprint
        model - model the API is created for
        name - name of the converted view_function to be registered with the `bp`
    """
    index_api = IndexAPI.as_view(f'{name}_index', model)
    list_api = ListAPI.as_view(f'{name}_list', model)
    bp.add_url_rule(f'/{name}/<int:id>', view_func=index_api)
    bp.add_url_rule(f'/{name}/', view_func=list_api)


# Registers model endpoints with Blueprint
for name_url, model in URL_MODEL_MAPPING.items():
    register_api_for_model(bp, model, name_url)
