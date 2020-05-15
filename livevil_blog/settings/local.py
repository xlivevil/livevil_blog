from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$2vb#)ikv^4*97yq^xynmhzssut_9ot*0p$8!=6qv%lhj+c200'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INTERNAL_IPS = ['127.0.0.1']


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
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
    }
}

# haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'xlivevil'
    },
}

# email设定

EMAIL_HOST = 'smtp.aliyun.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xlivevil@aliyun.com'
EMAIL_HOST_PASSWORD = 'gs$1@OzBca'
# EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
EMAIL_USE_SSL = True
EMAIL_FROM = 'xlivevil@aliyun.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# redis缓存
CACHES = {
    'default': {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": 'redis://@127.0.0.1:6379/0',
        "OPTION": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        }
    }
}
