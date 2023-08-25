"""
Django settings for web_server project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import time
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0j7dd(3o$r7ps+b27t9-p$#rri%55x^ckj(x#dpjnwxpdqiki8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']  # 此处应配置前端的地址
ALLOWED_EXTERNAL_OPENID_REDIRECT_DOMAINS = ['localhost', '0.0.0.0:8000', '127.0.0.1']

# openid 字段配置
LOGIN_URL = '/openid/login/'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = ''
OPENID_SSO_SERVER_URL = "XXXXX"
OPENID_CREATE_USERS = True
AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # 管理员站点， 你很快就会使用它
    'django.contrib.auth',  # 认证授权系统
    'django.contrib.contenttypes',  # 内容类型框架
    'django.contrib.sessions',  # 会话框架
    'django.contrib.messages',  # 消息框架
    'django.contrib.staticfiles',  # 管理静态文件的框架
    'channels',  # channels应用
    'rest_framework',
    "django_openid_auth",
    "django_celery_results",
    "django_celery_beat",  # 异步任务
    "inspection",  # 注册APP,
]

# 中间件配置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "dist")],
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

ROOT_URLCONF = 'web_server.urls'

WSGI_APPLICATION = 'web_server.wsgi.application'

# 设置ASGI应用
ASGI_APPLICATION = 'web_server.asgi.application'

# 设置通道层的通信后台 - 本地测试用
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# 数据库设置
DATABASES_DIR = os.path.join(os.path.dirname(BASE_DIR), 'database')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASES_DIR, 'inspection.sqlite')
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = True

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# REST_FRAMEWORK配置
REST_FRAMEWORK = {'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S"}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(DATABASES_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "dist/static"),  # 网页静态页面
]

IMAGE_URL = '/static/images/'
IMAGE_ROOT = os.path.join(DATABASES_DIR, 'static', 'images')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# scrapyd相关配置
START_SCRAPYD = True  # 是否交由django启动scrapyd
SCRAPYD_URL = "http://127.0.0.1:6800"
SCRAPYD_PATH = os.path.join(os.path.dirname(BASE_DIR), "crawler", "crawler_server")
# 向scrapyd提交的EGG路径
CRAWLER_EGG_PATH = os.path.join(os.path.dirname(BASE_DIR), "crawler", "crawler_script", "egg")
CRAWLER_PROJECT = "piracy_crawler"

# 日志文件的设置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_PATH = os.path.join(LOG_DIR, "django")  # 订单日志存放目录
# 若目录不存在则创建
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format':
            '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
            '[%(levelname)s]- %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    # 处理器
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 3,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 3,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    # 配置日志处理器
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',  # 日志器接收的最低日志级别
            'propagate': True,
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# 设置消息broker,格式为：db://user:password@host:port/dbname
# 如果redis安装在本机，使用localhost
# 如果docker部署的redis，使用redis://redis:6379
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

# celery时区设置，建议与Django settings中TIME_ZONE同样时区，防止时差
# Django设置时区需同时设置USE_TZ=True和TIME_ZONE = 'Asia/Shanghai'
# CELERY_TIMEZONE = TIME_ZONE

# 官方用来修复CELERY_ENABLE_UTC=False and USE_TZ = False 时时间比较错误的问题；
# 详情见：https://github.com/celery/django-celery-beat/pull/216/files
CELERY_DJANGO_CELERY_BEAT_TZ_AWARE = False

# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
CELERY_TASK_TIME_LIMIT = 180

# 支持数据库django-db和缓存django-cache存储任务状态及结果
CELERY_RESULT_BACKEND = "django-db"

# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = [
    'application/json',
]
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# 禁用所有速度限制
CELERY_DISABLE_RATE_LIMITS = True

# celery beat配置（周期性任务设置）
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_DJANGO_CELERY_BEAT_TZ_AWARE = False

# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

# celery 的启动工作数量设置
CELERY_WORKER_CONCURRENCY = 10

# 任务预取功能，就是每个工作的进程／线程在获取任务的时候，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
CELERYD_PREFETCH_MULTIPLIER = 10

# 本地测试
# CELERY_TASK_ALWAYS_EAGER = True

# 允许重试
CELERY_ACKS_LATE = True

# 单个任务的最大运行时间，超过就杀死
CELERYD_TASK_TIME_LEMIT = 12 * 30

# CELERY缓存
CELERY_MAX_CACHED_RESULTS = 10000
