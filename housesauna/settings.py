import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET', '')

DEBUG = False

# PROD SETTINGS
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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

EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = None
EMAIL_HOST_PASSWORD = os.getenv('SMTP_TEST', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL', '')
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

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
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'project.log'),
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        'housesauna': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

LAST_TO_VIEW = 3

METATAGS = {
    'house': {
        'title': 'Строительство домов из клееного бруса под ключ в Москве и области — проекты и цены',
        'description': ('Мы строим деревянные дома из клееного бруса для'
                        ' постояного проживания и делаем это качественно.'
                        ' Подберем для вас готовый проект или разработаем индивидуальный.'),
    },
    'sauna': {
        'title': 'Строительство бань из клееного бруса под ключ в Москве и области — проекты и цены',
        'description': ('Мы строим бани из клееного бруса и делаем это качественно. '
                        'Подберем для вас готовый проект или разработаем индивидуальный.'),
    }
}
