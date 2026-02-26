import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPhases:
    def test_list_phases_authenticated(self, consumer_client, innovation_phase):
        response = consumer_client.get('/api/phases/')
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_create_phase_as_admin(self, admin_client):
        data = {
            'title': 'Nueva Fase Admin',
            'description': 'Descripción de nueva fase',
            'order': 10,
        }
        response = admin_client.post('/api/phases/', data)
        assert response.status_code == 201
        assert response.data['title'] == 'Nueva Fase Admin'

    def test_create_phase_as_consumer(self, consumer_client):
        data = {
            'title': 'Fase No Permitida',
            'description': 'No debería crearse',
            'order': 99,
        }
        response = consumer_client.post('/api/phases/', data)
        assert response.status_code == 403

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get('/api/phases/')
        assert response.status_code in [401, 403]
