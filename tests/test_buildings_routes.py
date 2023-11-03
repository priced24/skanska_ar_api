import pytest
from tests.helpers import reset_test_database

@pytest.fixture(scope='module', autouse=True)
def add_data(app):
    """ add_data

    Module scoped fixture to populate the database with dummy data

    Parameters:
        app - app instance for testing
    """

    with app.app_context():
        from api.database import db_session
        from api.models import Building, Room, Sensor, SensorDataReadable
        reset_test_database()
        db_session.add(Building(name='building', description='desc'))
        db_session.commit()


class TestBuildingsRoutes:
    """ TestBuildingsRoutes

    Class containing tests related to making requests to the '/buildings' endpoint.
    """
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    url = '/buildings'

    def test_buildings_get(self, client):
        """ test_buildings_get

        Tests making a GET request to '/buildings'.
        """
        response = client.get(self.url, follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == [{
            'id': 1,
            'name': 'building',
            'description': 'desc',
            'rooms': [],
        }]

    def test_buildings_get_id(self, client):
        """ test_buildings_get_id

        Tests making a GET request to '/buidlings/<id>' with a known id.
        """
        response = client.get(f'{self.url}/1', follow_redirects=True)

        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 1,
            'name': 'building',
            'description': 'desc',
            'rooms': [],
        }

    def test_buildings_get_id_404(self, client):
        """ test_buildings_get_id_404

        Tests making a GET request to '/buildings/<id>' with a nonexistent id.
        """
        response = client.get(f'{self.url}/2', follow_redirects=True)
        assert response.status_code == 404

    def test_buidlings_post(self, client):
        """ test_buildings_post

        Tests making a POST request to '/buildings'.
        """
        data = {
            'name': 'building',
            'description': 'desc'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 200
        assert response.json == {
            'id': 2,
            'name': 'building',
            'description': 'desc',
            'rooms': [],
        }

    def test_buildings_post_400_empty(self, client):
        """ test_buildings_post

        Tests making a POST request to '/buildings' with empty body.
        """
        data = {}
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_buildings_post_400_name(self, client):
        """ test_buildings_post

        Tests making a POST request to '/buildings' with only 'name' in body.
        """
        data = {
            'name': 'building'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_buildings_post_400_description(self, client):
        """ test_buildings_post

        Tests making a POST request to '/buildings' with only 'description' in body.
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

    def test_buildings_post_400_random(self, client):
        """ test_buildings_post

        Tests making a POST request to '/buildings' with an additional key/value pair.
        """
        data = {
            'name': 'building',
            'description': 'desc',
            'random': 'data'
        }
        response = client.post(
            self.url, headers=self.headers, json=data, follow_redirects=True)
        assert response.content_type == self.mime_type
        assert response.status_code == 400
        assert response.json == {
            'message': 'Invalid raw body structure for request.'
        }

    def test_building_delete(self, client):
        """ test_building_delete

        Tests making a DELETE request to '/buildings/<id>' with a known id.
        """

        response = client.delete(
            f"{self.url}/1", follow_redirects=True)
        assert response.status_code == 204

    def test_buildings_delete_404(self, client):
        """ test_buildings_delete

        Tests making a DELETE request to '/buildings/<id>' with a nonexistent id.
        """
        response = client.delete(
            f'{self.url}/3', follow_redirects=True)
        assert response.status_code == 404