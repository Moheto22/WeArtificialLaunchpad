from rest_framework import viewsets, permissions
from apps.core.permissions import IsAdministrator
from .models import InnovationPhase
from .serializers import InnovationPhaseSerializer

class InnovationPhaseViewSet(viewsets.ModelViewSet):
    queryset = InnovationPhase.objects.filter(is_active=True)
    serializer_class = InnovationPhaseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdministrator()]
        return [permissions.IsAuthenticated()]
