from rest_framework import routers
from .views import ActivityLogViewSet

router = routers.DefaultRouter()
router.register('', ActivityLogViewSet, basename='activitylog')

urlpatterns = router.urls
