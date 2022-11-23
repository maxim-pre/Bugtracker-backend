from cgitb import lookup
from rest_framework_nested import routers

from .views import DeveloperViewSet, ProjectDeveloperViewSet, ProjectViewSet, TicketViewSet


router = routers.DefaultRouter()
router.register('developers', DeveloperViewSet, basename='developers')
router.register('projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
projects_router.register('tickets',TicketViewSet, basename='project-tickets')
projects_router.register('developers',ProjectDeveloperViewSet, basename='project-developers')

urlpatterns = router.urls + projects_router.urls