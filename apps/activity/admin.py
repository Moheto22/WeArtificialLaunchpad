from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('action', 'details', 'user__username')
    readonly_fields = ('user', 'action', 'details', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
