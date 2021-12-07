import logging
from logging import getLevelName

from django.conf import settings as django_settings


def __get_fc_as_fs_logging_level():
    logging_evel = getLevelName(getattr(django_settings, "FC_AS_FS_LOGGING_LEVEL"))
    return logging_evel if isinstance(logging_evel, int) else logging.INFO


FC_AS_FS_CONNECTION_MODEL = getattr(
    django_settings, "FC_AS_FS_CONNECTION_MODEL", "django_oidc_id_provider.Connection"
)
FC_AS_FS_LOGGING_LEVEL = __get_fc_as_fs_logging_level()
FC_AS_FS_ROUTE = getattr(django_settings, "FC_AS_FS_ROUTE", "")
FC_AS_FS_BASE_URL = django_settings.FC_AS_FS_BASE_URL
FC_AS_FS_ID = django_settings.FC_AS_FS_ID
FC_AS_FS_SECRET = django_settings.FC_AS_FS_SECRET
FC_AS_FS_CALLBACK_URL = django_settings.FC_AS_FS_CALLBACK_URL
