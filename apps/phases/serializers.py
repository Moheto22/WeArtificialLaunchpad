from rest_framework import serializers
from .models import InnovationPhase, PhaseField, PromptChunk

class PhaseFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhaseField
        fields = ['id', 'label', 'field_name', 'field_type', 'placeholder', 'required', 'order', 'list_of_options']

class PromptChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptChunk
        fields = ['id', 'content', 'is_optional', 'order']

class InnovationPhaseSerializer(serializers.ModelSerializer):
    fields = PhaseFieldSerializer(many=True, read_only=True)
    prompt_chunks = PromptChunkSerializer(many=True, read_only=True)

    class Meta:
        model = InnovationPhase
        fields = ['id', 'title', 'description', 'order', 'prompt_chunks', 'fields']
