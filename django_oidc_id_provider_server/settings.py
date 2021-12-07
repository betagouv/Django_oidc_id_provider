import os
from distutils.util import strtobool
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def getenv_bool(key: str, default: Optional[bool] = None) -> bool:
    """Obtains a boolean value from an environement variable

    Authorized values are casing variants of "true", "yes", "false" and "no" as well as
    0 and 1. Any other valuer will result in an error unless a default value
    is provided.

    If the environment variable does not exist and no default value is provided,
    an error will be thrown

    :param key: The name the the environment variable to load
    :param default: The default value to take if env var does not exist
    """
    var = os.getenv(key, default)

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


load_dotenv(verbose=True)

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("APP_SECRET")

DEBUG = getenv_bool("DEBUG", False)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_oidc_id_provider",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_oidc_id_provider_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_oidc_id_provider_server.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
