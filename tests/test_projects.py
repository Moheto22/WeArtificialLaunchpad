import pytest
from rest_framework.test import APIClient
from apps.activity.models import ActivityLog


@pytest.mark.django_db
class TestProjects:
    def test_create_project(self, consumer_client, consumer_user):
        data = {
            'name': 'Nuevo Proyecto',
            'description': 'Descripción del nuevo proyecto',
        }
        response = consumer_client.post('/api/projects/', data)
        assert response.status_code == 201
        assert response.data['name'] == 'Nuevo Proyecto'
        assert ActivityLog.objects.filter(
            user=consumer_user,
            action='CREATE_PROJECT',
        ).exists()

    def test_list_projects_only_own(self, consumer_client, consumer_user, admin_user, db):
        from apps.projects.models import Project
        Project.objects.create(user=consumer_user, name='Proyecto Consumer')
        Project.objects.create(user=admin_user, name='Proyecto Admin')

        response = consumer_client.get('/api/projects/')
        assert response.status_code == 200
        names = [p['name'] for p in response.data]
        assert 'Proyecto Consumer' in names
        assert 'Proyecto Admin' not in names

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get('/api/projects/')
        assert response.status_code in [401, 403]
