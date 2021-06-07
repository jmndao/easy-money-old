from django.apps import AppConfig


class DashboardConfig(AppConfig):
    # Using default django autofield primary key type
    default_auto_field = 'django.db.models.AutoField'
    name = 'dashboard'
