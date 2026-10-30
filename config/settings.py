"""Minimal bootstrap settings for P01-T01.

Typed environment configuration and production hardening belong to P01-T02.
These settings are deliberately limited to local bootstrap verification.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# This non-secret bootstrap value is replaced by the P01-T02 configuration boundary.
SECRET_KEY = "p01-t01-local-bootstrap-only"
DEBUG = True
ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "apps.core",
]

MIDDLEWARE: list[str] = []
ROOT_URLCONF = "config.urls"
TEMPLATES: list[dict[str, object]] = []
WSGI_APPLICATION = "config.wsgi.application"

# P01-T03 owns PostgreSQL configuration and migration foundations. SQLite is
# used only so Django can initialize for the bounded T01 system checks.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
