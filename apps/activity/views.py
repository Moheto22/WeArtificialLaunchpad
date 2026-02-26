from rest_framework import viewsets
from apps.core.permissions import IsAdministrator
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdministrator]
    queryset = ActivityLog.objects.all()
