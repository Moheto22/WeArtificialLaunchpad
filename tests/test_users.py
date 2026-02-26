import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.mark.django_db
class TestUsers:
    def test_list_users_as_admin(self, admin_client, admin_user, consumer_user):
        response = admin_client.get('/api/users/')
        assert response.status_code == 200
        usernames = [u['username'] for u in response.data]
        assert 'admin_user' in usernames
        assert 'consumer_user' in usernames

    def test_list_users_as_consumer(self, consumer_client, consumer_user):
        response = consumer_client.get('/api/users/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['username'] == consumer_user.username

    def test_create_user(self):
        client = APIClient()
        data = {
            'username': 'nuevo_usuario',
            'password': 'testpass123',
            'email': 'nuevo@test.com',
        }
        response = client.post('/api/users/', data)
        assert response.status_code == 201
        assert User.objects.filter(username='nuevo_usuario').exists()

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get('/api/users/')
        assert response.status_code in [401, 403]
