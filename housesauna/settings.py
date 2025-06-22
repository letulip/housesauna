import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET', '')

DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '158.160.183.146']

# PROD SETTINGS
# DEBUG = False
# ALLOWED_HOSTS = ['37.228.117.208', 'hs.letulip.ru', 'localhost']
ALLOWED_HOSTS = ['80.249.149.81', 'demo.domizkleenogobrusa.ru', 'www.domizkleenogobrusa.ru', 'domizkleenogobrusa.ru', 'localhost']
CSRF_TRUSTED_ORIGINS = ['https://80.249.149.81', 'https://www.domizkleenogobrusa.ru', 'https://domizkleenogobrusa.ru']

INSTALLED_APPS = [
    'houses.apps.HousesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'rest_framework_xml',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'housesauna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          os.path.join(BASE_DIR, 'templates')
          ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'csp.context_processors.nonce',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'housesauna.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSP_DEFAULT_SRC = ["'none'"]
CSP_BASE_URI = ["'self'"]
CSP_SCRIPT_SRC = [
  "'self'",
  "'unsafe-inline'",
  "https://api-maps.yandex.ru",
  "https://yandex.st",
  "https://yastatic.net",
]
CSP_SCRIPT_SRC_ELEM = [
  "'self'",
  "'unsafe-inline'",
  "https://mc.yandex.ru",
  "https://api-maps.yandex.ru",
  "https://yandex.st",
  "https://yastatic.net",
  "https://core-renderer-tiles.maps.yandex.net",
  "https://yastatic.net",
  "https://core-road-events-renderer.maps.yandex.net",
]
CSP_FRAME_SRC = [
  "'self'",
  "'unsafe-inline'",
  "https://mc.yandex.ru/",
  "https://yandex.ru",
  "https://www.yandex.ru",
  "https://youtube.com",
  "https://www.youtube.com",
]
CSP_STYLE_SRC = [
  "'self'",
  "'unsafe-inline'",
]
CSP_IMG_SRC = [
  "'self'",
  "http://www.w3.org",
  "data:",
  "https://mc.yandex.ru",
  "https://api-maps.yandex.ru",
  "https://core-renderer-tiles.maps.yandex.net",
  "https://core-jams-rdr-cache.maps.yandex.net",
  "https://core-road-events-renderer.maps.yandex.net",
]
CSP_CONNECT_SRC = [
  "'self'",
  "https://mc.yandex.ru",
]
CSP_FONT_SRC = [
  "'self'",
  "https://fonts.gstatic.com",
]
CSP_INCLUDE_NONCE_IN = ["script-src"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'ivladimirskiy@ya.ru'
EMAIL_HOST_PASSWORD = None
EMAIL_HOST_PASSWORD = os.getenv('SMTP_TEST', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@domizkleenogobrusa.ru'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} [{name}] {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'project.log'),
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        'housesauna': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'houses': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
