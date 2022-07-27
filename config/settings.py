from pathlib import Path
import os
import sys
import django_heroku


BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR / 'apps'))

SECRET_KEY = 'django-insecure-0&7t)dg*lnrlx^-31+-!_xl(+m(oxx-u)zn%-yo7238o=bz66v'

DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LIB_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_spectacular',
]

LOCAL_APPS = [
    'projects',
    'project_economic_indicators',
    'project_financing_sources',
    'project_taxes',
    'project_sales',
    'project_calculations',
    'account',
]

AUTH_USER_MODEL = 'account.User'

INSTALLED_APPS = DJANGO_APPS + LIB_APPS + LOCAL_APPS


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS=True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'projects.pagination.CustomPagination',
    'PAGE_SIZE': 30,

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S.%fZ",

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

DISABLE_COLLECTSTATIC=1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mvp_base_test',
#         'USER' : 'mvp_user',
#         'PASSWORD' : 'test!metadoor',
#         'HOST' : 'rc1b-ajj26k33iqbqcwj4.mdb.yandexcloud.net',
#         'PORT' : '6432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR / 'files')
MEDIA_URL = '/files/'

STATIC_ROOT = os.path.join(BASE_DIR / 'static')
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())