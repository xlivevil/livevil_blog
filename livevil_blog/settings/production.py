import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.xlivevil.com']

INTERNAL_IPS = ['170.106.13.74']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blog',
            'USER': 'django',
            'PASSWORD': os.environ['DJANGO_MYSQL_PASSWORD'],
            'HOST': '172.17.0.1',
            'PORT': '3306',
            'OPTION': {
                'charset': 'utf8mb4',
                'autocommit': True,
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            }
        },
    'mongodb':
        {
            'ENGINE': 'djongo',
            'ENFORCE_SCHEMA': True,
            'LOGGING': {
                'version': 1,
                'loggers': {
                    'djongo': {
                        'level': 'DEBUG',
                        'propogate': False,
                    }
                },
            },
            'NAME': 'djongo',
            'CLIENT': {
                'host': '172.17.0.1',
                'port': 27017,
            }
        }
}

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52    # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True

# haystack
HAYSTACK_CONNECTIONS = {
    'default':
        {
            'ENGINE': 'blog.elasticsearch5_ik_backend.Elasticsearch5IkSearchEngine',
            'URL': 'http://livevil_blog_elasticsearch:9200/',
            'INDEX_NAME': 'xlivevil'
        },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# email设定

EMAIL_HOST = 'smtp.aliyun.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xlivevil@aliyun.com'
EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_PASSWORD']
# EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
EMAIL_USE_SSL = True
EMAIL_FROM = 'xlivevil@aliyun.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = [('admin', 'xf_hyl@qq.com'), ('su', 'xlivevil@163.com')]
MANAGERS = ADMINS
SERVER_MAIL = 'xlivevil@aliyun.com'

# redis缓存
CACHES = {
    'default':
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ['DJANGO_REDIS_LOCATION'],
            'OPTION': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
}

# 日志配置

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':
        {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
    'filters':
        {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'missing_variable_error': {
                '()': 'livevil_blog.utils.log_filters.MissingVariableErrorFilter',
            }
        },
    'handlers':
        {
            'console':
                {
                    'level': 'INFO',
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
            'file':
                {
                    'level': 'WARNING',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(BASE_DIR, 'debug.log'),
                    'formatter': 'verbose',
                },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'formatter': 'verbose',
            }
        },
    'loggers':
        {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.file': {
                'handlers': ['file', 'mail_admins'],
                'level': 'WARNING',
                'propagate': True,
            },
            'django.template': {
                'level': 'DEBUG',
                'filters': ['missing_variable_error'],
            },
        },
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[DjangoIntegration(), RedisIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Django_storage
DEFAULT_FILE_STORAGE = 'netdisk.ibm_cos.MediaStorage'
STATICFILES_STORAGE = 'netdisk.ibm_cos.StaticStorage'

COS_BUCKET_NAME = os.environ['COS_BUCKET_NAME']
COS_ENDPOINT = os.environ['COS_ENDPOINT']
COS_API_KEY_ID = os.environ['COS_API_KEY_ID']
COS_SERVICE_CRN = os.environ['COS_SERVICE_CRN']
COS_AUTH_ENDPOINT = os.environ['COS_AUTH_ENDPOINT']
COS_CUSTOM_DOMAIN = os.environ['COS_CUSTOM_DOMAIN']

COMPRESS_URL = os.environ['COMPRESS_URL']
COMPRESS_STORAGE = STATICFILES_STORAGE

STATIC_URL = os.environ['STATIC_URL']
MEDIA_URL = os.environ['MEDIA_URL']

# grappelli
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
# 把admin的静态文件,由原来的admin目录,改为映射到static目录下的
GRAPPELLI_ADMIN_TITLE = '后台管理系统'    # 更改grappelli的登入title
