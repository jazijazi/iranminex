from django.apps import AppConfig


class InitialbordersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initialborders'

    from django.apps import AppConfig


    def ready(self):
        import initialborders.models.models
        import initialborders.signals
