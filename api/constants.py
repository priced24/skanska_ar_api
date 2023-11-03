from enum import IntEnum
from api.models import *


class StatusCode(IntEnum):
    """ StatusCode

    Enum class that defines some HTTP status codes
    """
    OK = 200
    NO_CONTENT = 204
    BAD_REQUEST = 400
    NOT_FOUND = 404


# Maps URL names to Model class for registering endpoints
URL_MODEL_MAPPING = {
    'buildings': Building,
    'rooms': Room,
    'sensors': Sensor,
    'sensor_data': SensorDataReadable,
}

DATETIME_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
TEST_DATA_JSON_RELATIVE_PATH = 'api/test_data/test_data.json'
