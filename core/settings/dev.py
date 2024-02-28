from .common import *

DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ['0.0.0.0']
SECRET_KEY = os.getenv("SECRET_KEY", "INSECURE_abc123!@#")
# DB_URL = os.getenv("DB_URL")

# debug toolbar settings
INTERNAL_IPS = ["127.0.0.1"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/assets/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "public/assets"),
    # os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Database
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
        
    #     # "ENGINE": "django.db.backends.mysql",
    #     # "HOST": "localhost",
    #     # "NAME": MYSQL_DATABASE_NAME,
    #     # "USER": MYSQL_USER,
    #     # "PASSWORD": MYSQL_PASSWORD,
    # }
    "default": dj_database_url.config(
        # mysql://USER:PASSWORD@HOST:PORT/NAME
        default="mysql://root:pwd@db/oeliks_db",
        # default=DB_URL,
        conn_max_age=600,
        # conn_health_checks=True,
    )
}

