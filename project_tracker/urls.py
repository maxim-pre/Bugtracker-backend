from cgitb import lookup
from rest_framework_nested import routers

from .views import DeveloperViewSet, ProjectDeveloperViewSet, ProjectViewSet, TicketViewSet, CommentViewSet, PersonalTicketViewSet


router = routers.DefaultRouter()
router.register('developers', DeveloperViewSet, basename='developers')
router.register('projects', ProjectViewSet, basename='projects')
router.register('tickets', PersonalTicketViewSet, basename='tickets')

projects_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
projects_router.register('tickets',TicketViewSet, basename='project-tickets')
projects_router.register('developers',ProjectDeveloperViewSet, basename='project-developers')

tickets_router = routers.NestedDefaultRouter(projects_router, 'tickets', lookup='ticket')
tickets_router.register('comments', CommentViewSet, basename='project-ticket-comments' )

urlpatterns = router.urls + projects_router.urls + tickets_router.urls