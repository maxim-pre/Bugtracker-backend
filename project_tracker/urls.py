from cgitb import lookup
from rest_framework_nested import routers

from project_tracker.serializers import DeveloperSerializer, TicketSerializer
from .views import DeveloperViewSet, ProjectViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register('developers', DeveloperViewSet, basename='developers')
router.register('projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
projects_router.register('tickets',TicketViewSet, basename='project-tickets')

urlpatterns = router.urls + projects_router.urls