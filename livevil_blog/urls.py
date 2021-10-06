from datetime import datetime
from typing import Any, Dict, Union

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.db.models.query import QuerySet
from django.urls import include, path

from blog.feed import AllPostsRssFeed
from blog.models import Post

info_dict: Dict[str, Union[datetime, QuerySet[Any], str]] = {
    'queryset': Post.objects.all(),
    'date_field': 'create_time',
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
    path(
        'sitemap.xml',
        sitemap, {'sitemaps': {
            'blog': GenericSitemap(info_dict, priority=0.6)
        }},
        name='django.contrib.sitemaps.views.sitemap'
    )
]

urlpatterns += i18n_patterns(
    path('grappelli/', include('grappelli.urls')),    # grappelli URLS
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('comments/', include('comments.urls')),
    path('comments/', include('django_comments.urls')),
    path('all/rss', AllPostsRssFeed(), name='rss'),
    path('api/', include('api.urls')),
    path('todo/', include('todo.urls')),
    path('netdisk/', include('netdisk.urls')),
    path('wiki/', include('wiki.urls')),
    path('contact/', include('contact_form.urls')),
    path('', include('blog.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
# TODO: error handler 模板和api两个版本 返回网页或JSON
