"""
Django settings for moodmo project.
"""

from pathlib import Path
from environs import Env

# Environment variables
# https://github.com/sloria/environs

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    "django-insecure-j$@j_n_)1+ooetp8ufu%2iaca(f=g%!l_vp!-#!x8ex13jeagz",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", [])

DJANGO_ADMIN_URL = env.str("DJANGO_ADMIN_URL", "admin/")


INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# Application definition

INSTALLED_APPS = [
    # 1st party
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    # Static files
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # 3rd party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Local
    "accounts",
    "pages",
    "moods",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_browser_reload",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "moodmo.urls"

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


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "moodmo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if env.bool("USE_POSTGRES", False):
    DATABASES = {
        "default": {
            "ENGINE": env.str(
                "POSTGRES_ENGINE",
                "django.db.backends.postgresql",
            ),
            "NAME": env.str("POSTGRES_DB", "moodmo_dev"),
            "USER": env.str("POSTGRES_USER", "django"),
            "PASSWORD": env.str("POSTGRES_PASSWORD", "root"),
            "HOST": env.str("POSTGRES_HOST", "postgres"),
            "PORT": env.str("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "data/db.sqlite3",
        }
    }


DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Cache
# https://docs.djangoproject.com/en/4.2/topics/cache/

if env.bool("USE_REDIS", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": env.list(
                "REDIS_LOCATION",
                "redis://redis:6379",
            ),
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

SITE_ID = 1

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Model to represent a User
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-user-model

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = env.str("LOGIN_REDIRECT_URL", "mood_list")
ACCOUNT_LOGOUT_REDIRECT_URL = env.str("ACCOUNT_LOGOUT_REDIRECT_URL", "home")

# Accounts related settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True

# Email backend
# https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend

EMAIL_HOST = env.str("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env.str("EMAIL_PORT", "1025")
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", 5)
