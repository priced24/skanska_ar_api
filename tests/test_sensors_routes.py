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
        from api.models import Building, Room, Sensor
        reset_test_database()
        db_session.add(Building(name='building', description='desc'))
        db_session.add(Room(name='room', description='desc', building_id=1))
        db_session.add(Sensor(name='sensor', description='desc', room_id=1))
        db_session.commit()


class TestSensorsRoutes:
    """ TestSensorsRoutes

    Class containing tests related to making requests to the '/sensors' endpoint.
    """
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    url = '/sensors'

    def test_sensors_get(self, client):
        """ test_sensors_get

        Tests making a GET request to '/sensors'.
        """
        response = client.get(self.url, follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == [{
            'id': 1,
            'name': 'sensor',
            'description': 'desc',
            'room': 'room',
            'room_id': 1,
            'data': [],
        }]

    def test_sensors_get_id(self, client):
        """ test_sensors_get_id

        Tests making a GET request to '/sensors/<id>' with a known id.
        """
        response = client.get(f'{self.url}/1', follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 1,
            'name': 'sensor',
            'description': 'desc',
            'room': 'room',
            'room_id': 1,
            'data': [],
        }

    def test_sensors_get_id_404(self, client):
        """ test_sensors_get_id_404

        Tests making a GET request to '/sensors/<id>' with a nonexistent id.
        """
        response = client.get(f'{self.url}/2', follow_redirects=True)
        assert response.status_code == 404

    def test_sensors_post(self, client):
        """ test_sensors_post

        Tests making a POST request to '/sensors'.
        """
        data = {
            'name': 'sensor',
            'description': 'desc',
            'room_id': 1,
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 2,
            'name': 'sensor',
            'description': 'desc',
            'room': 'room',
            'room_id': 1,
            'data': [],
        }

    def test_sensors_post_400_empty(self, client):
        """ test_sensors_post_400_empty

        Tests making a POST request to '/sensors' with empty body.
        """
        data = {}
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensors_post_400_name(self, client):
        """ test_sensors_post_400_name

        Tests making a POST request to '/sensors' with empty body.
        """
        data = {
            'name': 'sensor'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensors_post_400_description(self, client):
        """ test_sensors_post_400_description

        Tests making a POST request to '/sensors' with only 'description' in body.
        """
        data = {
            'description': 'desc'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensors_post_400_room_id(self, client):
        """ test_sensors_post_400_room_id

        Tests making a POST request to '/sensors' with only 'building_id' in body.
        """
        data = {
            'room_id': 1
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensors_post_400_random(self, client):
        """ test_sensors_post_400_random

        Tests making a POST request to '/sensors' with an additional key/value pair.
        """
        data = {
            'name': 'sensor',
            'description': 'desc',
            'room_id': 1,
            'random': 'data'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_sensors_delete(self, client):
        """test_sensors_delete

        Tests deleting a DELETE request to '/sensors/<id>' with a known id.
        """
        response = client.delete(f'{self.url}/1', follow_redirects=True)
        assert response.status_code == 204

    def test_sensors_delete_404(self, client):
        """test_sensors_delete_404

        Tests making a DELETE request to '/sensors/<id>' with a nonexistent id.
        """
        response = client.delete(
            f'{self.url}/3', follow_redirects=True)
        assert response.status_code == 404 