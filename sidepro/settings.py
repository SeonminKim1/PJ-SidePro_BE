"""
Django settings for sidepro project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


if os.environ.get('IS_LOCAL') == 'TRUE':
    ALLOWED_HOSTS = []
else: # for Production
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')



INSTALLED_APPS = [
    'corsheaders',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'user',
    'project',
    'chat',
    'recommand',
    'rest_framework',
    'rest_framework_simplejwt',
]

# CRON TAB
if os.environ.get('IS_LOCAL')=='TRUE':
    pass
else: # for production
    INSTALLED_APPS.append('django_crontab')
    CRONJOBS=[
    ('*/1 * * * *', 'recommand.cron.recommend_crontab', '>> /sidepro_be/log/crontab.log'),
    ]


### ASGI - Channels, Redis..
ASGI_APPLICATION = 'sidepro.asgi.application'

if os.environ.get('IS_LOCAL') == 'TRUE':
    redis_ip = '127.0.0.1'
else: # for production
    redis_ip = '3.37.194.222'

# Channel layers => redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer', 
        'CONFIG': {
            "hosts": [(redis_ip, 6379)],
        },
    },
}


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# FE의 주소값을 입력해주어야한다.
if os.environ.get('IS_LOCAL') == 'TRUE':
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
    "http://sidepro.shop.s3-website.ap-northeast-2.amazonaws.com",
    "http://sidepro.shop",
    "http://sidepro-sub.shop.s3-website.ap-northeast-2.amazonaws.com",
    "http://sidepro-sub.shop",
    ]

ROOT_URLCONF = 'sidepro.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates') # myprojet/templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'sidepro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

## Default
# =========== Setting Key by my_settings.py ===========

if os.environ.get('IS_LOCAL') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("LOCAL_ENGINE"),
            'NAME': os.environ.get("LOCAL_NAME"), # Schema Name
            'USER': os.environ.get("LOCAL_USER"),
            'PASSWORD': os.environ.get("LOCAL_PASSWORD"), # PASSWORD NAME
            'HOST':os.environ.get("LOCAL_HOST"),
            'PORT':os.environ.get("LOCAL_PORT"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("ENGINE"),
            'NAME': os.environ.get("NAME"), # Schema Name
            'USER': os.environ.get("USER"),
            'PASSWORD': os.environ.get("PASSWORD"), # PASSWORD NAME
            'HOST':os.environ.get("HOST"),
            'PORT':os.environ.get("PORT"),
        }
    }

# MYSQL_DATABASE
# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get("MYSQL_ENGINE"),
#         'NAME': os.environ.get("MYSQL_NAME"), # Schema Name
#         'USER': os.environ.get("MYSQL_USER"),
#         'PASSWORD': os.environ.get("MYSQL_PASSWORD"), # PASSWORD NAME
#         'HOST':os.environ.get("MYSQL_HOST"),
#         'PORT':os.environ.get("MYSQL_PORT"),
#     }
# }
### SQLITE DB 사용 희망시 아래 주석 풀어서 사용
# """
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }"""

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 원래 True KOREA Time을 위한 False 설정


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [ # 기본적인 view 접근 권한 지정
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [ # session 혹은 token을 인증 할 클래스 설정
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [ # request.data 속성에 액세스 할 때 사용되는 파서 지정
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
}

AUTH_USER_MODEL = 'user.User' # app.model

# JWT 관련 세부 설정 (생략 가능)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'TOKEN_USER_CLASS': 'user.User'
}

# # https://docs.djangoproject.com/en/1.11/topics/logging/
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }