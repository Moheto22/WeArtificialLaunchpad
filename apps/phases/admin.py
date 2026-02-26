from django.contrib import admin
from .models import InnovationPhase, PhaseField, PromptChunk

class PhaseFieldInline(admin.TabularInline):
    model = PhaseField
    extra = 1
    prepopulated_fields = {"field_name": ("label",)}

class PromptChunkInline(admin.TabularInline):
    model = PromptChunk
    extra = 1

@admin.register(InnovationPhase)
class InnovationPhaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    inlines = [PhaseFieldInline, PromptChunkInline]

@admin.register(PhaseField)
class PhaseFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'phase', 'field_type', 'required', 'order')
    list_filter = ('phase', 'field_type')
    search_fields = ('label', 'field_name')

@admin.register(PromptChunk)
class PromptChunkAdmin(admin.ModelAdmin):
    list_display = ('phase', 'order', 'is_optional')
    list_filter = ('phase',)
