SECRET_KEY = 'fake-key'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'api',
    'rest_framework',
    'common',
    'activities',
    'comment',
    'post',
    'test',
)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'unicooo_postgres_sql',
        'USER': 'windson',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
        'CHARSET': 'UTF-8',
    }
}
