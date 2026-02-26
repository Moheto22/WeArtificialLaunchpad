from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Project(TimeStampedModel):
    """
    A project created by a user to group their innovation phases.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
