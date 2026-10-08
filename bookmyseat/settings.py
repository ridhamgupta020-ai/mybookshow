"""
Django settings for bookmyseat project.
"""

from pathlib import Path
import os

import dj_database_url


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

IS_VERCEL = os.environ.get("VERCEL") == "1"


# ============================================================
# HELPERS
# ============================================================

def environment_list(name, default=""):
    return [
        value.strip()
        for value in os.environ.get(name, default).split(",")
        if value.strip()
    ]


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. "
        "Add SECRET_KEY to your Vercel Environment Variables."
    )


DEBUG = os.environ.get(
    "DEBUG",
    "False" if IS_VERCEL else "True",
).lower() in ("1", "true", "yes", "on")


if IS_VERCEL and DEBUG:
    raise RuntimeError("DEBUG must be False on Vercel.")


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = environment_list(
    "ALLOWED_HOSTS",
    "mybookshow-kohl.vercel.app",
)

if not IS_VERCEL:
    ALLOWED_HOSTS.extend([
        "localhost",
        "127.0.0.1",
        "[::1]",
    ])


# Automatically allow Vercel URLs
for variable in (
    "VERCEL_URL",
    "VERCEL_PROJECT_PRODUCTION_URL",
):
    vercel_host = os.environ.get(variable, "").strip()

    if vercel_host:
        if vercel_host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(vercel_host)


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = environment_list(
    "CSRF_TRUSTED_ORIGINS",
    "https://mybookshow-kohl.vercel.app",
)


for variable in (
    "VERCEL_URL",
    "VERCEL_PROJECT_PRODUCTION_URL",
):
    vercel_host = os.environ.get(variable, "").strip()

    if vercel_host:
        vercel_origin = f"https://{vercel_host}"

        if vercel_origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(vercel_origin)


# ============================================================
# HTTPS / SECURITY
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SECURE_SSL_REDIRECT = not DEBUG

SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "users",
    "movies",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# AUTH
# ============================================================

AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/login/"


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ============================================================
# MEDIA
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "bookmyseat.urls"


# ============================================================
# TEMPLATES
# ============================================================

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


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "bookmyseat.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


if DATABASE_URL:

    default_database = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
    )

    if default_database.get("ENGINE") == "django.db.backends.postgresql":
        default_database.setdefault("OPTIONS", {})
        options = default_database.get("OPTIONS")
        if options is None:
            options = {}
            default_database["OPTIONS"] = options
        options["sslmode"] = "require"

    if default_database.get("PORT") == 6543:
        default_database["DISABLE_SERVER_SIDE_CURSORS"] = True

    DATABASES = {
        "default": default_database,
    }

elif IS_VERCEL or not DEBUG:

    raise RuntimeError(
        "DATABASE_URL must be set when DEBUG is disabled."
    )

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND":
        "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"