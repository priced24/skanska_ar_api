from datetime import datetime
import pytest
from tests.helpers import reset_test_database


@pytest.fixture(scope='module', autouse=True)
def add_data(app):
    """ add_data

    Module scoped fixture to populate the database with dummy data

    Parameter:
        app - app instance for testing
    """

    with app.app_context():
        from api.database import db_session
        from api.models import Building, Room, Sensor, SensorDataReadable
        reset_test_database()
        db_session.add(Building(name='building', description='desc'))
        db_session.add(Room(name='room', description='desc', building_id=1))
        db_session.add(Sensor(name='sensor', description='desc', room_id=1))
        db_session.add(SensorDataReadable(
            value='1',
            units='C',
            sensor_id=1,
            datetime=datetime.strptime(
                '2023-03-20 00:00:00', '%Y-%m-%d %H:%M:%S')
        ))
        db_session.commit()


class TestSensorDataRoutes:
    """ TestSensorDataRoutes

    Class containing tests related to making requests to the '/sensor_data' endpoint.
    """
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    url = '/sensor_data'

    def test_sensor_data_get(self, client):
        """ test_sensor_data_get

        Tests making a GET request to '/sensor_data'.
        """
        response = client.get(self.url, follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == [{
            'id': 1,
            'sensor': 'sensor',
            'sensor_id': 1,
            'value': '1',
            'units': 'C',
            'sensor_id': 1,
            'datetime': '2023-03-20 00:00:00',
        }]

    def test_sensor_data_get_id(self, client):
        """ test_sensor_data_get_id

        Tests making a GET request to '/sensor_data/<id>' with a known id.
        """
        response = client.get(f'{self.url}/1', follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 1,
            'sensor': 'sensor',
            'sensor_id': 1,
            'value': '1',
            'units': 'C',
            'sensor_id': 1,
            'datetime': '2023-03-20 00:00:00',
        }

    def test_sensor_data_get_id_404(self, client):
        """ test_sensor_data_get_id_404

        Tests making a GET request to '/sensor_data/<id>' with a nonexistent id.
        """
        response = client.get(f'{self.url}/2', follow_redirects=True)
        assert response.status_code == 404

    def test_sensor_data_post(self, client):
        """ test_sensor_data_post

        Tests making a POST request to '/sensor_data'.
        """
        data = {
            'value': '1',
            'units': 'C',
            'sensor_id': 1,
            'datetime': '2023-03-20 00:00:00',
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 2,
            'sensor': 'sensor',
            'sensor_id': 1,
            'value': '1',
            'units': 'C',
            'sensor_id': 1,
            'datetime': '2023-03-20 00:00:00',
        }

    def test_sensor_data_post_400_empty(self, client):
        """ test_sensor_data_post_400_empty

        Tests making a POST request to '/sensor_data' with empty body.
        """
        data = {}
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_post_400_value(self, client):
        """ test_sensor_data_post_400_value

        Tests making a POST request to '/sensor_data' with only 'value' in body.
        """
        data = {
            'value': '1'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_post_400_units(self, client):
        """ test_sensor_data_post_400_units

        Tests making a POST request to '/sensor_data' with only 'units' in body.
        """
        data = {
            'units': 'C'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_post_400_sensor_id(self, client):
        """ test_sensor_data_post_400_sensor_id

        Tests making a POST request to '/sensor_data' with only 'sensor_id' in body.
        """
        data = {
            'senosr_id': 1
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_post_400_datetime(self, client):
        """ test_sensor_data_post_400_datetime

        Tests making a POST request to '/sensor_data' with only 'datetime' in body.
        """
        data = {
            'datetime': '2023-03-20 00:00:00'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_post_400_random(self, client):
        """ test_sensor_data_post_400_random

        Tests making a POST request to '/sensor_data' with an additional key/value pair.
        """
        data = {
            'value': '1',
            'units': 'C',
            'sensor_id': 1,
            'datetime': '2023-03-20 00:00:00',
            'random': 'data'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensor_data_delete(self, client):
        """test_sensor_data_delete

        Tests deleting a DELETE request to '/sensor_data/<id>' with a known id.
        """
        response = client.delete(f'{self.url}/1', follow_redirects=True)
        assert response.status_code == 204

    def test_sensor_data_delete_404(self, client):
        """test_sensor_data_delete_404

        Tests making a DELETE request to '/sensor_data/<id>' with a nonexistent id.
        """
        response = client.delete(
            f'{self.url}/3', follow_redirects=True)
        assert response.status_code == 404
