from .base import *

with open(secret_file) as json_data:
    d = json.load(json_data)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '300/minute',
        'user': '500/minute'
    }
}

ALLOWED_HOSTS = ["*"]

DEBUG = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'unicooo_sunkist',
        'USER': 'Windson',
        'PASSWORD': d['pythonanywhere'],
        'HOST': 'Windson.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'CHARSET': 'UTF-8',
    }
}
