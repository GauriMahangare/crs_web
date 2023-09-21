from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "crs_web.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import crs_web.users.signals  # noqa: F401
        except ImportError:
            pass
