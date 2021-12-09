import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "django_oidc_id_provider_test_bed.settings"
)

application = get_wsgi_application()
