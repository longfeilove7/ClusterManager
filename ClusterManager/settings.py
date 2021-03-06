#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
from celery.schedules import crontab
from datetime import timedelta

# -*- coding: utf-8 -*-
"""
Django settings for ClusterManager project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!oki@#(pwr6w7&1m-ypyukd+d(0kut_hi@8fd4k&o2m5ev*i-z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    #for django-jet
    'jet.dashboard',
    'jet',
    #django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    #for app
    'HostManager',
    #for celery
    'django_celery_beat',
    'django_celery_results',
    #for swagger
    'rest_framework_swagger',
    #for django-guardian
    'guardian',
    #for django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.baidu',
    'allauth.socialaccount.providers.douban',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.weixin',
    #给django添加css样式
    'widget_tweaks',#可以自定义CSS
    'crispy_forms',#傻瓜式
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ClusterManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ClusterManager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clustermanager',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'neunn',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'  #default language

#TIME_ZONE = 'Asia/Shanghai'
#配置成上海时区导致django-celery-beat不能正常工作，每天凌晨3点到12点不发送任务
TIME_ZONE = 'UTC'
USE_I18N = True

USE_L10N = True

USE_TZ = True



LANGUAGES = (
    ('en', ('English')),
    ('zh-Hans', ('中文简体')),
    ('zh-Hant', ('中文繁體')),
)

#翻译文件所在目录，需要手工创建
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.i18n", )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

# TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

#django-jet themes
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_ITEMS = [
    {
        'label': '权限管理',
        'app_label': 'auth',
        'items': [
            {
                'name': 'group'
            },
            {
                'name': 'user'
            },
        ]
    },
    {
        'label': '任务结果',
        'app_label': 'django_celery_results',
        'items': [
            {
                'name': 'taskresult'
            },
        ]
    },
    {
        'label':
        '计划任务',
        'app_label':
        'django_celery_beat',
        'items': [
            {
                'name': 'crontabschedule'
            },
            {
                'name': 'intervalschedule'
            },
            {
                'name': 'periodictask'
            },
            {
                'name': 'solarschedule'
            },
        ]
    },
]
CELERY_ENABLE_UTC = True
#CELERY_TIMEZONE = 'UTC'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
#CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_BEAT_SCHEDULE = {
    #周期任务
    'task-ping': {
        'task': 'HostManager.Tasks.fping',
        'schedule': timedelta(seconds=300),  #每30秒执行一次
        'args': ()  #must be list or tuple.
    },
    # # 定时任务
    # 'task-two': {
    #     'task': 'HostManager.Tasks.printHello',
    #     'schedule': crontab(minute=0, hour='*/3,10-19'),
    #      'args':()
    # },
    # #共享任务
    # 'task-one': {
    #     'task': 'HostManager.Tasks.add',
    #     'schedule': crontab(), #每1分钟执行一次
    #      'args':(4, 4)
    # },
    #增加任务
}

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',  #django-guardian
    #'allauth.account.auth_backends.AuthenticationBackend', #django-allauth
)

#django-allauth
SITE_ID = 1 # 1为数据库django-site中的ID

# django-allauth基本设定
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' #使用用户名或邮件登录
ACCOUNT_EMAIL_REQUIRED = True
#LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_REDIRECT_URL = '/index' #用户登录重定向
ACCOUNT_LOGOUT_REDIRECT_URL ='/'#用户登出重定向
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1 #邮件验证有效期,单位天
ACCOUNT_EMAIL_VERIFICATION ="mandatory" #不激活的账户不允许登录
ACCOUNT_USERNAME_BLACKLIST = ['admin','neunn'] #用户不能使用的用户名列表
ACCOUNT_USERNAME_MIN_LENGTH= 3 #用户名最小长度

# django-allauth邮箱设定
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '277784408@qq.com' # 你的 QQ 账号和授权码
EMAIL_HOST_PASSWORD = 'ipbgjcznsoqtbied'
EMAIL_USE_TLS = True  # 这里必须是 True，否则发送不成功
EMAIL_FROM = '277784408@qq.com' # 你的 QQ 账号
DEFAULT_FROM_EMAIL = '277784408@qq.com'

#CRISPY_TEMPLATE_PACK = 'bootstrap4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#SESSION AGE
SESSION_COOKIE_AGE = 60*60 #60分钟
SESSION_EXPIRE_AT_BROWSER_CLOSE = False #浏览器关闭是否过期
SESSION_SAVE_EVERY_REQUEST = True

