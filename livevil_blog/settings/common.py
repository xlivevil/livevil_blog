"""
Django settings for livevil_blog project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    # External apps that need to go before django's
    'grappelli',
    # Django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admindocs',
    # Local apps
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'comments.apps.BlogCommentsConfig',
    'api',
    # External apps
    'django_comments',
    'crispy_forms',
    'reversion',
    'debug_toolbar',
    'pure_pagination',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.windowslive',
    'allauth.socialaccount.providers.baidu',
    'haystack',
    'rest_framework',
    'mptt',
    'drf_yasg',
    'django_filters',
    'compressor',
    'subdomains',
    'djongo',
    'contact_form',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'livevil_blog.urls'

# A dictionary of urlconf module paths, keyed by their subdomain.
SUBDOMAIN_URLCONFS = {
    None: 'livevil_blog.urls',  # no subdomain, e.g. ``example.com``
    'www': 'livevil_blog.urls',
    'api': 'livevil_blog.urls.api',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'), ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'livevil_blog.wsgi.application'
ASGI_APPLICATION = 'livevil_blog.asgi.application'

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# TODO: 解决本地数据库timezone问题
USE_TZ = False

LANGUAGES = (('zh-hans', _('中文简体')), ('en', _('English')), ('ja', _('日本語')))

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

X_FRAME_OPTIONS = 'sameorigin'

# 多数据库联用
DATABASE_ROUTERS = [
    'livevil_blog.database_router.MongoDBRouter',
]

# 增加第三方登录支持
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.EmailBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 扩展默认User功能
AUTH_USER_MODEL = 'users.User'

# crispy-forms的模式
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# django-pure-pagination设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# allauth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # 可以邮箱或用户名登录
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'  # 设置登录后跳转链接
LOGOUT_REDIRECT_URL = '/'  # 设置登出后跳转链接

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # 确认邮件截至时间
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）”或“否（none）”之一

ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180  # 邮件发送后的冷却时间(以秒为单位)

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5  # 登录尝试失败的次数
ACCOUNT_LOGIN_ON_GET = False  # 用户登出

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 从上次失败的登录尝试，用户被禁止尝试登录的持续时间

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False  # 更改或设置密码后是否自动退出

ACCOUNT_LOGIN_ON_PASSWORD_RESET = False  # 更改为True，用户将在重置密码后自动登录

ACCOUNT_SESSION_REMEMBER = None  # 控制会话的生命周期，可选项还有:False,True

ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False  # 用户注册时是否需要输入邮箱两遍

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # 用户注册时是否需要用户输入两遍密码

ACCOUNT_USERNAME_BLACKLIST = [
    'admin',
]  # 用户不能使用的用户名列表

ACCOUNT_UNIQUE_EMAIL = True  # 加强电子邮件地址的唯一性

ACCOUNT_USERNAME_MIN_LENGTH = 2  # 用户名允许的最小长度的整数

SOCIALACCOUNT_AUTO_SIGNUP = True  # 使用从社会帐户提供者检索的字段(如用户名、邮件)来绕过注册表单

ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # 设置退出登录后跳转链接

# APPEND_SLASH=False

# haystack

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CUSTOM_HIGHLIGHTER = 'blog.highlighter.Highlighter'

SECURE_BROWSER_XSS_FILTER = True

COMMENTS_APP = 'comments'

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
    10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'EXCEPTION_HANDLER': ['rest_framework.views.exception_handler'],
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION':
    'v1',
    # 限流
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',
        'user': '20/min'
    },
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# django-compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    # creates absolute urls from relative ones
    'compressor.filters.css_default.CssAbsoluteFilter',
    # css minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

# grappelli
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
# 把admin的静态文件,由原来的admin目录,改为映射到static目录下的
GRAPPELLI_ADMIN_TITLE = '后台管理系统'  # 更改grappelli的登入title

# session的存储配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 设置session失效时间,单位为秒
SESSION_COOKIE_AGE = 60 * 30
