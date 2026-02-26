from django.contrib import admin
from .models import PhaseResponse

@admin.register(PhaseResponse)
class PhaseResponseAdmin(admin.ModelAdmin):
    list_display = ('project', 'phase', 'created_at')
    list_filter = ('phase', 'project__user')
    search_fields = ('project__name', 'phase__title')
    readonly_fields = ('created_at', 'updated_at')
