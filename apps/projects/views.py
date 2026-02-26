from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from apps.activity.models import ActivityLog

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action="CREATE_PROJECT",
            details=f"Proyecto creado: {project.name}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
