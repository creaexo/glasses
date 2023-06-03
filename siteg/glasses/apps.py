from django.apps import AppConfig


class GlassesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'glasses'
    verbose_name = '    Магазин'


class LensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lenses'
