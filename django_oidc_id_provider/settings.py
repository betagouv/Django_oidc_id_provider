import logging
from distutils.util import strtobool
from logging import getLevelName
from typing import Any, Optional

from django.conf import settings as django_settings


def __get_fc_as_fs_logging_level():
    logging_level = getLevelName(
        getattr(django_settings, "FC_AS_FS_LOGGING_LEVEL", "INFO")
    )
    return logging_level if isinstance(logging_level, int) else logging.INFO


def __get_bool(obj: Any, key: str, default: Optional[bool] = None) -> bool:
    """Obtains a boolean value from an environement variable

    Authorized values are casing variants of "true", "yes", "false" and "no" as well as
    0 and 1. Any other valuer will result in an error unless a default value
    is provided.

    If the environment variable does not exist and no default value is provided,
    an error will be thrown

    :param key: The name the the environment variable to load
    :param default: The default value to take if env var does not exist
    """
    var = getattr(obj, key, default)

    if var is None:
        raise ValueError(
            f"{key} is not present in environment variables "
            "and no default value was provided"
        )

    if isinstance(var, bool):
        return var

    try:
        return bool(strtobool(var))
    except ValueError:
        if default is not None:
            return default
        else:
            raise ValueError(
                f"{key} does not have a valid boolean value; authorized values are "
                'any casing of ["true", "yes", "false", "no"] as well as 0 and 1.'
            )


FC_AS_FS_LOGGING_LEVEL = __get_fc_as_fs_logging_level()
FC_AS_FS_ROUTE = getattr(django_settings, "FC_AS_FS_ROUTE", "")
FC_AS_FS_BASE_URL = django_settings.FC_AS_FS_BASE_URL
FC_AS_FS_ID = django_settings.FC_AS_FS_ID
FC_AS_FS_SECRET = django_settings.FC_AS_FS_SECRET
FC_AS_FS_CALLBACK_URL = django_settings.FC_AS_FS_CALLBACK_URL
FC_CONNECTION_AGE = int(getattr(django_settings, "FC_CONNECTION_AGE", 300))

FC_AS_FS_CONNECTION_MODEL = getattr(
    django_settings, "FC_AS_FS_CONNECTION_MODEL", "django_oidc_id_provider.Connection"
)
FC_AS_FS_SESSION_KEY_SAVE = getattr(
    django_settings, "FC_AS_FS_SESSION_KEY_SAVE", "connection"
)

FC_AS_FS_GET_PREFERRED_USERNAME = __get_bool(
    django_settings, "GET_PREFERRED_USERNAME_FROM_FC", True
)
