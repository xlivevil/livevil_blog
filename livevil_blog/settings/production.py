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
        'USER': '',
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
        'URL': 'http://liveivl_blog_elasticsearch:9200/',
        'INDEX_NAME': 'xlivevil'
    },
}
