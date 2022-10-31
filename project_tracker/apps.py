from django.apps import AppConfig


class ProjectTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_tracker'

    def ready(self) -> None:
        import project_tracker.signals
