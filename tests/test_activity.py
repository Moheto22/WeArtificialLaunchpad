import pytest
from rest_framework.test import APIClient
from apps.activity.models import ActivityLog


@pytest.mark.django_db
class TestActivity:
    def test_admin_can_list_activity(self, admin_client, admin_user, consumer_user):
        ActivityLog.objects.create(
            user=consumer_user,
            action='CREATE_PROJECT',
            details='Proyecto de prueba creado',
            ip_address='127.0.0.1',
        )
        ActivityLog.objects.create(
            user=admin_user,
            action='GENERATE_PROMPT',
            details='Prompt generado',
            ip_address='127.0.0.1',
        )

        response = admin_client.get('/api/activity/')
        assert response.status_code == 200
        assert len(response.data) >= 2

    def test_consumer_cannot_access_activity(self, consumer_client):
        response = consumer_client.get('/api/activity/')
        assert response.status_code == 403

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get('/api/activity/')
        assert response.status_code in [401, 403]
