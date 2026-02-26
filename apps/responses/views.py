from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import PhaseResponse
from .serializers import PhaseResponseSerializer
from apps.phases.utils import generate_prompt
from apps.activity.models import ActivityLog

class PhaseResponseViewSet(viewsets.ModelViewSet):
    serializer_class = PhaseResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PhaseResponse.objects.filter(project__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phase = serializer.validated_data['phase']
        form_data = serializer.validated_data['form_data']
        
        # Generate the prompt
        generated_prompt_text = generate_prompt(phase, form_data)
        
        # Save response
        response_obj = serializer.save(generated_prompt=generated_prompt_text)
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action="GENERATE_PROMPT",
            details=f"Prompt generado para fase: {phase.title} en proyecto: {response_obj.project.name}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response(self.get_serializer(response_obj).data, status=status.HTTP_201_CREATED)
