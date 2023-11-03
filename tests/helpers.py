
def reset_test_database():
    """ reset_test_database

    Helper function to delete all records across all the tables in the database.
    """
    from api.models import Building, Room, Sensor, SensorDataReadable
    Building.query.delete()
    Room.query.delete()
    Sensor.query.delete()
    SensorDataReadable.query.delete()
