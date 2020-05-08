from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['106.13.5.251']

INTERNAL_IPS = ['106.13.5.251']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ['DJANGO_MYSQL_PASSWORD'],
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
        'URL': 'http://livevil_blog_elasticsearch:9200/',
        'INDEX_NAME': 'xlivevil'
    },
}

# email设定

EMAIL_HOST = 'smtp.aliyun.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xlivevil@aliyun.com'
EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_PASSWORD']
# EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
EMAIL_USE_SSL = True
EMAIL_FROM = 'xlivevil@aliyun.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# redis缓存
CACHES = {
    'default': {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": os.environ['DJANGO_REDIS_LOCATION'],
        "OPTION": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        }
    }
}