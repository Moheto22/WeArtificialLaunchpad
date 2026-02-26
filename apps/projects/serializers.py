from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'user', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
