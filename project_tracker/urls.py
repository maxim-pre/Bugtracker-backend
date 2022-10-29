from rest_framework_nested import routers

from project_tracker.serializers import DeveloperSerializer
from .views import DeveloperViewSet, ProjectViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tickets', TicketViewSet, basename='tickets')
router.register('developers', DeveloperViewSet, basename='developers')

urlpatterns = router.urls