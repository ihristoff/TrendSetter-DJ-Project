from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TrendSetter.articles'

    def ready(self):
        import TrendSetter.articles.signals
