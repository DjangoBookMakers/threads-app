from django.apps import AppConfig


class ThreadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "threads"

    def ready(self):
        import threads.signals
