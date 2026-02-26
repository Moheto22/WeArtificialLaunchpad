from django.db import models
from apps.core.models import TimeStampedModel
from apps.projects.models import Project
from apps.phases.models import InnovationPhase

class PhaseResponse(TimeStampedModel):
    """
    Stores the user's input for a specific phase within a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='responses')
    phase = models.ForeignKey(InnovationPhase, on_delete=models.CASCADE)
    form_data = models.JSONField(verbose_name="Datos del Formulario")
    generated_prompt = models.TextField(verbose_name="Prompt Generado")

    def __str__(self):
        return f"Respuesta {self.phase.title} - {self.project.name}"

    class Meta:
        verbose_name = "Respuesta de Fase"
        verbose_name_plural = "Respuestas de Fases"
