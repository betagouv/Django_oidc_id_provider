from os.path import join as path_join

from django.urls import include, path

from django_oidc_id_provider import settings
from django_oidc_id_provider.views import fc_authorize, fc_callback

urlpatterns = [
    path(
        path_join(settings.FC_AS_FS_ROUTE, ""),
        include(
            [
                path("fc_authorize/", fc_authorize, name="fc_authorize"),
                path("callback/", fc_callback, name="fc_callback"),
            ]
        ),
    ),
]
