from django.contrib import admin
from .models import Project
from apps.responses.models import PhaseResponse

class PhaseResponseInline(admin.TabularInline):
    model = PhaseResponse
    extra = 0
    show_change_link = True
    readonly_fields = ('phase', 'created_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    inlines = [PhaseResponseInline]
