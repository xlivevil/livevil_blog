from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']

INTERNAL_IPS = ['127.0.0.1']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blog',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
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
                'host': '127.0.0.1',
                'port': 27017,
            }
        }
}

# haystack
HAYSTACK_CONNECTIONS = {
    'default':
        {
            'ENGINE': 'blog.elasticsearch5_ik_backend.Elasticsearch5IkSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'xlivevil'
        },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# email设定

EMAIL_HOST = 'smtp.aliyun.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xlivevil@aliyun.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
EMAIL_USE_SSL = True
EMAIL_FROM = 'xlivevil@aliyun.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = [('admin', 'xlivevil@aliyun.com')]
MANAGERS = ADMINS
SERVER_MAIL = 'xlivevil@aliyun.com'

# redis缓存
CACHES = {
    'default':
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://@127.0.0.1:6379/0',
            'OPTION': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
}
