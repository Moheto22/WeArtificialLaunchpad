from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    """
    Custom user model for the innovation platform.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
    surname = models.CharField(max_length=255, verbose_name="Apellidos", blank=True)
    company = models.CharField(max_length=255, verbose_name="Empresa", blank=True, null=True)
    
    is_administrator = models.BooleanField(default=False, verbose_name="Es Administrador")
    is_consumer = models.BooleanField(default=True, verbose_name="Es Consumidor")

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")

    def __str__(self):
        return f"{self.username} ({'Admin' if self.is_administrator else 'Consumer'})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
