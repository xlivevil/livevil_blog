"""livevil_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from blog.feed import AllPostsRssFeed

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('comments/', include('comments.urls')),
    path('', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
    path('all/rss', AllPostsRssFeed(), name="rss"),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('comments/', include('django_comments.urls')),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
