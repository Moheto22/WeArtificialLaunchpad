from rest_framework import routers
from .views import PhaseResponseViewSet

router = routers.DefaultRouter()
router.register('', PhaseResponseViewSet, basename='response')

urlpatterns = router.urls
