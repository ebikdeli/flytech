from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from . import signals


### for more information about how to implement signals:
# https://docs.djangoproject.com/en/3.2/ref/applications/#django.apps.AppConfig.ready
# https://docs.djangoproject.com/en/3.2/ref/signals/#post-migrate
