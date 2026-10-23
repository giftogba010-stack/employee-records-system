"""
Django settings for employee_records_system.

Local development: SQLite
Heroku production: JawsDB MySQL
"""

import os
from pathlib import Path

import dj_database_url


# ============================================================
# 1. BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 2. SECURITY SETTINGS
# ============================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-only-change-me"
)

DEBUG = os.environ.get(
    "DEBUG", "False"
).lower() == "true"

# Heroku application domain
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,gitapp-1665f67d4768.herokuapp.com"
    ).split(",")
    if host.strip()
]

# CSRF protection for HTTPS requests
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://gitapp-1665f67d4768.herokuapp.com"
    ).split(",")
    if origin.strip()
]


# ============================================================
# 3. INSTALLED APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Employee Records Application
    "employees",
]


# ============================================================
# 4. MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Static file handling on Heroku
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# 5. URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "employee_records_system.urls"


# ============================================================
# 6. TEMPLATE CONFIGURATION
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
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


# ============================================================
# 7. WSGI APPLICATION
# ============================================================

WSGI_APPLICATION = "employee_records_system.wsgi.application"


# ============================================================
# 8. DATABASE CONFIGURATION
# ============================================================
#
# On Heroku:
#   Connect automatically to JawsDB MySQL using JAWSDB_URL.
#
# On local computer:
#   Use SQLite when JAWSDB_URL is not provided.
#
# Do not hardcode your JawsDB username or password here.
# ============================================================

JAWSDB_URL = os.environ.get("JAWSDB_URL")

if JAWSDB_URL:

    # Production database: JawsDB MySQL
    DATABASES = {
        "default": dj_database_url.parse(
            JAWSDB_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    # Local development database: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# 9. PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = []


# ============================================================
# 10. LANGUAGE AND TIME ZONE
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# ============================================================
# 11. STATIC FILES CONFIGURATION
# ============================================================

STATIC_URL = "/static/"

# Optional project-level static directory
STATICFILES_DIRS = (
    [BASE_DIR / "static"]
    if (BASE_DIR / "static").exists()
    else []
)

# Heroku collectstatic destination
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise static file storage
STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# 12. DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# 13. LOGIN AND LOGOUT SETTINGS
# ============================================================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# ============================================================
# 14. HEROKU HTTPS AND COOKIE SECURITY
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https"
)

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# ============================================================
# 15. PRODUCTION SECURITY
# ============================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ============================================================
# END OF SETTINGS
# ============================================================