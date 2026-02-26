from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Apps
    path('api/users/', include('apps.users.urls')),
    path('api/phases/', include('apps.phases.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/responses/', include('apps.responses.urls')),
    path('api/activity/', include('apps.activity.urls')),
]
