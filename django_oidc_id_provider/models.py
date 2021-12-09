from datetime import timedelta

from django.db import models
from django.utils import timezone

from django_oidc_id_provider import settings


def default_connection_expiration_date():
    now = timezone.now()
    return now + timedelta(seconds=settings.FC_CONNECTION_AGE)


class Connection(models.Model):
    state = models.TextField()  # FS
    nonce = models.TextField(default="No Nonce Provided")
    expires_on = models.DateTimeField(default=default_connection_expiration_date)
    access_token = models.TextField(default="No token provided")

    @property
    def is_expired(self):
        return self.expires_on < timezone.now()

    class Meta:
        swappable = "FC_AS_FS_CONNECTION_MODEL"
