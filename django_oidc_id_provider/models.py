from django.db import models


class Connection(models.Model):
    state = models.TextField()  # FS
    nonce = models.TextField(default="No Nonce Provided")
    CONNECTION_TYPE = (("FS", "FC as FS"), ("FI", "FC as FI"))
    connection_type = models.CharField(
        max_length=2, choices=CONNECTION_TYPE, default="FI", blank=False
    )

    class Meta:
        swappable = "FC_AS_FS_CONNECTION_MODEL"
