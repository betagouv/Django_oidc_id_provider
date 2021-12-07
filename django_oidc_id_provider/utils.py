from typing import TypeVar

from django.apps import apps
from django.conf import settings

from django_oidc_id_provider.models import Connection

V = TypeVar("V", bound=Connection)


def get_connection_model() -> V:
    return apps.get_model(settings.AUTH_USER_MODEL)
