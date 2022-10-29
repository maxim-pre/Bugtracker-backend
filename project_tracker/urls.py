from rest_framework_nested import routers
from .views import ProjectViewSet

router = routers.DefaultRouter()
router.register('projects',ProjectViewSet, basename='projects')


urlpatterns = router.urls