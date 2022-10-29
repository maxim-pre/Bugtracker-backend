from rest_framework_nested import routers
from .views import ProjectViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tickets', TicketViewSet, basename='tickets')


urlpatterns = router.urls