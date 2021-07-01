from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from blog.feed import AllPostsRssFeed

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('comments/', include('comments.urls')),
    path('accounts/', include('allauth.urls')),
    path('all/rss', AllPostsRssFeed(), name="rss"),
    path("api/", include("api.urls")),
    path('todo/', include('todo.urls')),
    path('netdisk/', include('netdisk.urls')),
    path('wiki/', include('wiki.urls')),
    path('contact/', include('contact_form.urls')),
    path('', include('blog.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))
                   ] + urlpatterns
