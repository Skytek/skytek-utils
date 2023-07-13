# pylint: disable=invalid-name
import os

if not os.environ.get("INTERCONNECT_SKIP_DJANGO", False):
    try:
        from django.conf import settings as django_settings
    except ImportError:
        django_settings = None
else:
    django_settings = None


class Settings:
    """Settings provider for interconnect client and jwt"""

    def get_value(self, conf_name):
        if hasattr(django_settings, conf_name):
            return getattr(django_settings, conf_name)
        return os.environ.get(conf_name)

    @property
    def INTERCONNECT_ENVIRONMENT_DOMAIN(self):
        value = self.get_value("INTERCONNECT_ENVIRONMENT_DOMAIN")
        if not value:
            raise ValueError("Setting INTERCONNECT_ENVIRONMENT_DOMAIN is required")
        return value

    @property
    def INTERCONNECT_USE_SSL(self):
        value = self.get_value("INTERCONNECT_ENVIRONMENT_DOMAIN")
        return value is None or value

    @property
    def INTERCONNECT_JWT_ENCODE_KEY(self):
        value = self.get_value("INTERCONNECT_JWT_ENCODE_KEY")
        if not value:
            raise ValueError("Setting INTERCONNECT_JWT_ENCODE_KEY is required")
        return value

    @property
    def INTERCONNECT_MODULE_NAME(self):
        value = self.get_value("INTERCONNECT_MODULE_NAME")
        if not value:
            raise ValueError("Setting INTERCONNECT_MODULE_NAME is required")
        return value


settings = Settings()
