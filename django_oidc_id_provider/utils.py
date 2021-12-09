from typing import TypeVar

from django.apps import apps

from django_oidc_id_provider import settings
from django_oidc_id_provider.models import Connection

V = TypeVar("V", bound=Connection)


def get_connection_model() -> V:
    return apps.get_model(settings.FC_AS_FS_CONNECTION_MODEL)
