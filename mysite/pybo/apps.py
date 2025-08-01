from django.apps import AppConfig


class PyboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mysite.pybo'

    def ready(self):
        import mysite.pybo.signals
