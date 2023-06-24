from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # run cron every time app start
    def ready(self):
        from api.scheduler import cron
        cron.start()
