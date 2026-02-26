from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    """
    Records user activity for traceability.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=255, verbose_name="Acción")
    details = models.TextField(verbose_name="Detalles")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ['-timestamp']
