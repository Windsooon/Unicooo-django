from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = "common_app"

    def ready(self):
        import common.signals
