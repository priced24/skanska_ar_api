# JSON schemas that define request bodies for different models
from .models import *

get_schema = {
    'type': 'object',
    'properties': {
        'df': {
            'type': 'string',
            'format': 'date-time',
        },
        'dt': {
            'type': 'string',
            'format': 'date-time',
        },
    },
    'additionalProperties': False,
}

# JSON schema for the Building model
building_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
    },
    'required': [
        'name', 'description',
    ],
    'additionalProperties': False,
}

# JSON schema for Room model
room_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'building_id': {
            'type': 'integer',
        },
    },
    'required': [
        'name', 'description', 'building_id',
    ],
    'additionalProperties': False,
}

# JSON schema for Sensor model
sensor_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'room_id': {
            'type': 'integer',
        },
    },
    'required': [
        'name', 'description', 'room_id',
    ],
    'additionalProperties': False,
}

# JSON schema for SensorDataReadable
sensor_data_schema = {
    'type': 'object',
    'properties': {
        'value': {
            'type': 'string',
        },
        'units': {
            'type': 'string',
        },
        'sensor_id': {
            'type': 'integer',
        },
        'datetime': {
            'type': 'string',
            'format': 'date-time',
        }
    },
    'required': [
        'value', 'units', 'sensor_id', 'datetime',
    ],
    'additionalProperties': False,
}


# Maps models to their JSON schema
# Should this be coupled more closely to the models?
# For instance should each model have a text field,
# that stores their corresponding JSON schema as a string
SCHEMA_MAPPING = {
    Building: building_schema,
    Room: room_schema,
    Sensor: sensor_schema,
    SensorDataReadable: sensor_data_schema
}
