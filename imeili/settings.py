#coding=utf8
"""
Django settings for imeili project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o^_#^$8++3s&qe+kjf&x)ypw-m(5l_+oa@dksnf_&dnzp@r64j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'braces',
    'rest_framework',
    'bootstrap3',
    'accounts',
    'employees',
    'members',
    'weixin',
    'products',
    'cashier',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'imeili.urls'

WSGI_APPLICATION = 'imeili.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


if 'SERVER_SOFTWARE' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'sqld.duapp.com',
            'PORT': '4050',
        }
    }

    db_name = ""
    api_key = ""
    secret_key = ""
    myauth = "%s-%s-%s"%(api_key, secret_key, db_name)

    AUTH_QR_CODE_REDIS_KWARGS = {
    "host": "redis.duapp.com",
    "port": 80,
    'password':myauth,
}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'imeili',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT   = os.path.join(BASE_DIR,'static').replace('\\', '/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, './static/').replace('\\','/'),)
#Templates
TEMPLATE_DIRS = (
     os.path.join(BASE_DIR, 'templates'),
)


#atuth
AUTH_USER_MODEL='employees.Employee'

LOGIN_REDIRECT_URL='/'

#email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}


#GRAPPELLI SETTINGS
GRAPPELLI_ADMIN_TITLE = u'美颜会员管理系统'