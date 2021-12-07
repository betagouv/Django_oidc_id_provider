import logging

from django.conf import settings
from django.contrib import messages as django_messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

import jwt
from jwt.api_jwt import ExpiredSignatureError
import requests as python_request
from secrets import token_urlsafe

from django_oidc_id_provider.utils import get_connection_model

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


Connection = get_connection_model()


def fc_authorize(request):
    connection = Connection.objects.get(pk=request.session["connection"])

    connection.state = token_urlsafe(16)
    connection.nonce = token_urlsafe(16)
    connection.connection_type = "FS"
    connection.save()

    fc_base = settings.FC_AS_FS_BASE_URL
    fc_id = settings.FC_AS_FS_ID
    fc_callback_uri = f"{settings.FC_AS_FS_CALLBACK_URL}/callback"
    fc_scopes = [
        "openid",
        "email",
        "gender",
        "birthdate",
        "birthplace",
        "given_name",
        "family_name",
        "birthcountry",
    ]
    if settings.GET_PREFERRED_USERNAME_FROM_FC:
        fc_scopes.append("preferred_username")

    parameters = (
        f"response_type=code"
        f"&client_id={fc_id}"
        f"&redirect_uri={fc_callback_uri}"
        f"&scope={'%20'.join(fc_scopes)}"
        f"&state={connection.state}"
        f"&nonce={connection.nonce}"
        f"&acr_values=eidas1"
    )

    authorize_url = f"{fc_base}/authorize?{parameters}"

    return redirect(authorize_url)


def fc_callback(request):
    fc_base = settings.FC_AS_FS_BASE_URL
    fc_callback_uri = f"{settings.FC_AS_FS_CALLBACK_URL}/callback"
    fc_callback_uri_logout = f"{settings.FC_AS_FS_CALLBACK_URL}/logout-callback"
    fc_id = settings.FC_AS_FS_ID
    fc_secret = settings.FC_AS_FS_SECRET
    state = request.GET.get("state")

    try:
        connection = Connection.objects.get(state=state)
    except Connection.DoesNotExist:
        log.info("FC as FS - This state does not seem to exist")
        log.info(state)
        return HttpResponseForbidden()

    if connection.is_expired:
        log.info("408: FC connection has expired.")
        return render(request, "408.html", status=408)

    code = request.GET.get("code")
    if not code:
        log.info("403: No code has been provided.")
        return HttpResponseForbidden()

    token_url = f"{fc_base}/token"
    payload = {
        "grant_type": "authorization_code",
        "redirect_uri": fc_callback_uri,
        "client_id": fc_id,
        "client_secret": fc_secret,
        "code": code,
    }
    headers = {"Accept": "application/json"}

    request_for_token = python_request.post(token_url, data=payload, headers=headers)

    def fc_error(log_msg):
        log.error(log_msg)
        django_messages.error(
            request,
            "Nous avons rencontré une erreur en tentant d'interagir avec "
            "France Connect. C'est probabablement temporaire. Pouvez-vous réessayer "
            "votre requête ?",
        )

        return redirect(reverse("new_mandat"))

    try:
        content = request_for_token.json()
    except ValueError:  # not a valid JSON
        return fc_error(
            f"Request to {token_url} failed. Status code: "
            f"{request_for_token.status_code}, body: {request_for_token.text}"
        )

    connection.access_token = content.get("access_token")
    if connection.access_token is None:
        return fc_error(
            f"No access_token return when requesting {token_url}. JSON response: "
            f"{repr(content)}"
        )

    connection.save()
    fc_id_token = content.get("id_token")

    try:
        decoded_token = jwt.decode(
            fc_id_token,
            settings.FC_AS_FS_SECRET,
            audience=settings.FC_AS_FS_ID,
            algorithm="HS256",
        )
    except ExpiredSignatureError:
        log.info("403: token signature has expired.")
        return HttpResponseForbidden()

    if connection.nonce != decoded_token.get("nonce"):
        log.info("403: The nonce is different than the one expected.")
        return HttpResponseForbidden()

    if connection.is_expired:
        log.info("408: FC connection has expired.")
        return render(request, "408.html", status=408)

    usager, error = get_user_info(connection)
    if error:
        django_messages.error(request, error)
        return redirect("espace_aidant_home")

    connection.usager = usager
    connection.save()

    logout_base = f"{fc_base}/logout"
    logout_id_token = f"id_token_hint={fc_id_token}"
    logout_state = f"state={state}"
    logout_redirect = f"post_logout_redirect_uri={fc_callback_uri_logout}"
    logout_url = f"{logout_base}?{logout_id_token}&{logout_state}&{logout_redirect}"
    return redirect(logout_url)


def get_user_info(connection: Connection) -> tuple:
    pass
