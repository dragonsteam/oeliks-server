from .celery import app

# from .celery import app as celery_app

# __all__ = ('celery_app',)

# mysql
import pymysql

pymysql.install_as_MySQLdb()