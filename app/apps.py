from django.apps import AppConfig


class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Import the periodic tasks setup code here
        from .setup_periodic_tasks import setup_periodic_tasks

        # Call the setup_periodic_tasks function
        setup_periodic_tasks()
