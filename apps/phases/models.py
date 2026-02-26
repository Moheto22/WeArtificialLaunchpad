from django.db import models
from apps.core.models import TimeStampedModel

class InnovationPhase(TimeStampedModel):
    """
    Represents a phase in the innovation process (e.g., Ideation, Validation).
    """
    title = models.CharField(max_length=255, verbose_name="Título de la Fase")
    description = models.TextField(verbose_name="Descripción")
    # prompt_template removed as requested.
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Fase de Innovación"
        verbose_name_plural = "Fases de Innovación"
        ordering = ['order']


class PhaseField(models.Model):
    """
    Dynamic fields for an Innovation Phase form.
    """
    FIELD_TYPES = (
        ('text', 'Texto Corto'),
        ('number', 'Número'),
        ('boolean', 'Booleano'),
        ('dropdown', 'Desplegable'),
        ('multi-select', 'Selección Múltiple'),
    )

    phase = models.ForeignKey(InnovationPhase, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=255, verbose_name="Etiqueta del Campo")
    field_name = models.SlugField(max_length=255, help_text="Nombre técnico (ej: 'idea_principal').")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text', verbose_name="Tipo de Campo")
    placeholder = models.CharField(max_length=255, blank=True, null=True, verbose_name="Placeholder")
    required = models.BooleanField(default=True, verbose_name="Obligatorio")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    list_of_options = models.JSONField(null=True, blank=True, verbose_name="Lista de opciones")

    def __str__(self):
        return f"{self.label} ({self.phase.title})"

    class Meta:
        verbose_name = "Campo de Formulario"
        verbose_name_plural = "Campos de Formulario"
        ordering = ['order']


class PromptChunk(models.Model):
    """
    Represents a static text chunk of a prompt, to be interleaved with PhaseFields.
    Logic: Chunk 0 + Field 0 + Chunk 1 + Field 1 ...
    """
    phase = models.ForeignKey(InnovationPhase, related_name='prompt_chunks', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Contenido del Fragmento", blank=True)
    is_optional = models.BooleanField(default=False, verbose_name="Es Opcional")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    def __str__(self):
        return f"Chunk {self.order} for {self.phase.title}"

    class Meta:
        verbose_name = "Fragmento de Prompt"
        verbose_name_plural = "Fragmentos de Prompt"
        ordering = ['order']
