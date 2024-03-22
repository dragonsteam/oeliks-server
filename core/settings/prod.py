from .common import *

DEBUG = False
ALLOWED_HOSTS = ["django"]
SECRET_KEY = os.getenv("SECRET_KEY")

# Database
DATABASES = {
    "default": dj_database_url.config(
        # default=DB_URL,
        default="mysql://root:pwd@db/oeliks_db",
        conn_max_age=600,
    )
}

# Static files
STATIC_URL = "/assets/"
STATIC_ROOT = os.path.join(BASE_DIR, "public/assets")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# # HTTPS settings
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# # HSTS settings
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
