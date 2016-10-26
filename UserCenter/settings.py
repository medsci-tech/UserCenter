"""
Django settings for UserCenter project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import mongoengine
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^qo29%1$$+w_flyv6^8%$!9^=3a4*vdw&gwtbk^cg8o(54^qw&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin',
    # 'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
############
# SESSIONS #
############

SESSION_CACHE_ALIAS = 'default'                         # Cache to store session data if using the cache session backend.
SESSION_COOKIE_NAME = 'sessionid'                       # Cookie name. This can be whatever you want.
SESSION_COOKIE_AGE = 60 * 5 * 24                             # Age of cookie, in seconds (default: 2 weeks). Now is 5 minutes.
SESSION_COOKIE_DOMAIN = None                            # A string like ".example.com", or None for standard domain cookie.
SESSION_COOKIE_SECURE = False                           # Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_PATH = '/'                               # The path of the session cookie.
SESSION_COOKIE_HTTPONLY = True                          # Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
SESSION_SAVE_EVERY_REQUEST = True                      # Whether to save the session data on every request.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True                  # Whether a user's session cookie expires when the Web browser is closed.
SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # The module to store session data
SESSION_FILE_PATH = None                                # Directory to store session files if using the file session module. If None, the backend will use a sensible default.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'  # class to serialize session data


ROOT_URLCONF = 'UserCenter.urls'

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
                #全局变量输出到模板，比如登录者的信息
                'UserCenter.global_templates.configParam',
                "django.template.context_processors.static",    #静态资源
            ],
        },
    },
]

WSGI_APPLICATION = 'UserCenter.wsgi.application'


# Database
DATABASES = {
    'default' : {
        #'ENGINE' : 'mongoengine',
        #'NAME' : 'my_database',
        'OPTIONS' : {
            'socketTimeoutMS' : 500,
        }
    }
}
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# MongoDB settings
MONGODB_USER = 'med_dev'
MONGODB_PASSWD = 'md_dev_2016'
MONGODB_HOST = 'dds-2zedefa8064299841.mongodb.rds.aliyuncs.com:3717'
MONGODB_NAME = 'md_usercenter'
MONGODB_PREFIX = 'md_' #集合前缀
MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (MONGODB_USER, MONGODB_PASSWD, MONGODB_HOST, MONGODB_NAME)

mongoengine.connect(MONGODB_NAME, host=MONGODB_DATABASE_HOST,connect=False)
AUTHENTICATION_BACKENDS = (
    'mongoengine.auth.MongoEngineBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "common_static"),
)
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads').replace('\\', '/')
# 上传文件目录设置
UPLOAD_URL = '/uploads/'
UPLOAD_ROOT = os.path.join(BASE_DIR, 'uploads')