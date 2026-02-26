import pytest
from rest_framework.test import APIClient
from apps.activity.models import ActivityLog
from apps.responses.models import PhaseResponse


@pytest.mark.django_db
class TestResponses:
    def test_create_response_generates_prompt(self, consumer_client, project, innovation_phase):
        data = {
            'project': project.id,
            'phase': innovation_phase.id,
            'form_data': {
                'campo_1': 'Mi idea innovadora',
                'campo_2': 'tecnología sostenible',
            },
        }
        response = consumer_client.post('/api/responses/', data, format='json')
        assert response.status_code == 201
        assert response.data['generated_prompt'] != ''
        assert 'Mi idea innovadora' in response.data['generated_prompt']

    def test_create_response_logs_activity(self, consumer_client, consumer_user, project, innovation_phase):
        data = {
            'project': project.id,
            'phase': innovation_phase.id,
            'form_data': {
                'campo_1': 'Idea para logging',
                'campo_2': 'sostenibilidad',
            },
        }
        consumer_client.post('/api/responses/', data, format='json')
        assert ActivityLog.objects.filter(
            user=consumer_user,
            action='GENERATE_PROMPT',
        ).exists()

    def test_list_responses_only_own(self, consumer_client, consumer_user, admin_user, project, innovation_phase, db):
        from apps.projects.models import Project
        admin_project = Project.objects.create(user=admin_user, name='Proyecto Admin')
        PhaseResponse.objects.create(
            project=project,
            phase=innovation_phase,
            form_data={'campo_1': 'valor consumer'},
            generated_prompt='prompt consumer',
        )
        PhaseResponse.objects.create(
            project=admin_project,
            phase=innovation_phase,
            form_data={'campo_1': 'valor admin'},
            generated_prompt='prompt admin',
        )

        response = consumer_client.get('/api/responses/')
        assert response.status_code == 200
        prompts = [r['generated_prompt'] for r in response.data]
        assert 'prompt consumer' in prompts
        assert 'prompt admin' not in prompts

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get('/api/responses/')
        assert response.status_code in [401, 403]
