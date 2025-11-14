from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"

    def ready(self):
        """Configure admin site when app is ready."""
        from django.contrib import admin

        admin.site.site_header = "Панель управления Max"
        admin.site.site_title = "Max Админ"
        admin.site.index_title = "Добро пожаловать в панель управления"
