from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from apps.projects.models import Project

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    show_change_link = True

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Roles de Plataforma', {'fields': ('is_administrator', 'is_consumer')}),
        ('Información Adicional', {'fields': ('company', 'name', 'surname')}),
    )
    list_display = UserAdmin.list_display + ('is_administrator', 'is_consumer', 'company')
    list_filter = UserAdmin.list_filter + ('is_administrator', 'is_consumer')
    inlines = [ProjectInline]
