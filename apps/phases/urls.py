from rest_framework import routers
from .views import InnovationPhaseViewSet

router = routers.DefaultRouter()
router.register('', InnovationPhaseViewSet, basename='innovationphase')

urlpatterns = router.urls
