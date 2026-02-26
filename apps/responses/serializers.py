from rest_framework import serializers
from .models import PhaseResponse

class PhaseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhaseResponse
        fields = ['id', 'project', 'phase', 'form_data', 'generated_prompt', 'created_at', 'updated_at']
        read_only_fields = ['generated_prompt', 'created_at', 'updated_at']
