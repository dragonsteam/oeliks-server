import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

load_dotenv()


# useful functions


def get_list(text):
    if not text:
        return []
    return [item.strip() for item in text.split(",")]


# def get_bool_from_env(name, default_value):
#     if name in os.environ:
#         value = os.environ[name]
#         try:
#             return ast.literal_eval(value)
#         except ValueError as e:
#             raise ValueError(f"{value} is an invalid value for {name}") from e
#     return default_value


# def get_url_from_env(name, *, schemes=None) -> Optional[str]:
#     if name in os.environ:
#         value = os.environ[name]
#         message = f"{value} is an invalid value for {name}"
#         URLValidator(schemes=schemes, message=message)(value)
#         return value
#     return None

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
if not TELEGRAM_BOT_TOKEN:
    raise ImproperlyConfigured("TELEGRAM_BOT_TOKEN is empty, please check environment variables.")


BASE_DIR = Path(__file__).resolve().parent.parent.parent

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('uz', _('Uzbek')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    # "django_seed",
    "django_telegram_login",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware", #lan
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["public"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Password validation

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

# LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# restframework
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60 * 24),
}

AUTH_USER_MODEL = "api.User"

# DJOSER = {
#     'SERIALIZERS': {
#         'user_create': 'core.serializers.UserCreateSerializer',
#         'user': 'core.serializers.UserSerializer',
#         'current_user': 'core.serializers.UserSerializer',
#     }
# }

# REDIS_BASE_URL = 'redis://redis:6379'
REDIS_BASE_URL = "redis://localhost:6379"

# # celery settings
CELERY_BROKER_URL = f"{REDIS_BASE_URL}/1"  # /1

CELERY_BEAT_SCHEDULE = {
    # 'notifyCustomers': {
    #     'task': 'api.tasks.notify_customers',
    #     'schedule': 5, # every five seconds
    #     # 'schedule': crontab(minute='*/15') # every 15 minutes
    #     # 'schedule': crontab(day_of_week=1, hour=7, minute=30) # every monday at 7:30 am
    #     'args': ['hello world'],
    # },
    "update_trucks": {
        "task": "api.tasks.update_trucks",
        "schedule": 5 * 60,
    },
    # 'logTrailers': {
    #     'task': 'api.tasks.log_trailers',
    #     'schedule': 2 * 60
    # }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_BASE_URL}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# GRAPHENE = {
#     "SCHEMA": "api.schema.schema"
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/general.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",  # str.format()
        }
    },
}
