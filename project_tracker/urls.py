from rest_framework_nested import routers

from project_tracker.serializers import DeveloperSerializer
from .views import DeveloperViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register('developers', DeveloperViewSet, basename='developers')
router.register('projects', ProjectViewSet, basename='projects')


urlpatterns = router.urls