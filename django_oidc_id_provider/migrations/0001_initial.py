# Generated by Django 3.2.10 on 2021-12-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.TextField()),
                ("nonce", models.TextField(default="No Nonce Provided")),
                (
                    "connection_type",
                    models.CharField(
                        choices=[("FS", "FC as FS"), ("FI", "FC as FI")],
                        default="FI",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "swappable": "FC_AS_FS_CONNECTION_MODEL",
            },
        ),
    ]
