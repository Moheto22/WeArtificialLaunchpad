import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.phases.models import InnovationPhase, PhaseField, PromptChunk
from apps.projects.models import Project


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username='admin_user',
        password='testpass123',
        is_administrator=True,
        is_consumer=False,
    )


@pytest.fixture
def consumer_user(db):
    return User.objects.create_user(
        username='consumer_user',
        password='testpass123',
        is_administrator=False,
        is_consumer=True,
    )


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def consumer_client(consumer_user):
    client = APIClient()
    client.force_authenticate(user=consumer_user)
    return client


@pytest.fixture
def innovation_phase(db):
    phase = InnovationPhase.objects.create(
        title='Fase de Prueba',
        description='Descripción de prueba',
        is_active=True,
        order=1,
    )
    PhaseField.objects.create(
        phase=phase,
        label='Campo 1',
        field_name='campo_1',
        field_type='text',
        order=0,
    )
    PhaseField.objects.create(
        phase=phase,
        label='Campo 2',
        field_name='campo_2',
        field_type='text',
        order=1,
    )
    PromptChunk.objects.create(phase=phase, content='Introduce tu idea: ', is_optional=False, order=0)
    PromptChunk.objects.create(phase=phase, content=' con enfoque en: ', is_optional=False, order=1)
    PromptChunk.objects.create(phase=phase, content=' resultado esperado.', is_optional=False, order=2)
    return phase


@pytest.fixture
def project(db, consumer_user):
    return Project.objects.create(
        user=consumer_user,
        name='Proyecto de Prueba',
        description='Descripción del proyecto de prueba',
    )
