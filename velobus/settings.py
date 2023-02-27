# Velobus
# Copyright (C) 2023  Manuel Tondeur

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "9ng(s5x7fde7=vhns6ro$n(r1lbm5ey&h4+ap)&xnf879bc$6t"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

if os.environ.get("DJANGO_HOST", False):
    ALLOWED_HOSTS.append(os.environ.get("DJANGO_HOST"))
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ.get('DJANGO_HOST')}")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "subscription",
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

ROOT_URLCONF = "velobus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "velobus.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "fr-be"

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "assets",
]

STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails_debug"

LOGIN_REDIRECT_URL = "/#/list"

EMAIL_HOST = os.getenv("VELOBUS_EMAIL_HOST")
EMAIL_PORT = int(os.getenv("VELOBUS_EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("VELOBUS_EMAIL_USE_TLS", True)
EMAIL_FROM = os.getenv("VELOBUS_FROM_EMAIL")
EMAIL_HOST_USER = os.getenv("VELOBUS_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("VELOBUS_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("VELOBUS_FROM_EMAIL")

FORM_TITLE = os.environ.get("FORM_TITLE", "Vélobus")
SCHEDULE_COMMENT = os.environ.get("SCHEDULE_COMMENT", "")
MAP_CENTER = os.environ.get("MAP_CENTER", [50.46574, 4.86696])
MAP_ZOOM = os.environ.get("MAP_ZOOM", 12)
