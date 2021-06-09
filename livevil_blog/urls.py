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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from api.views import PostViewSet, CommentViewSet
from blog.feed import AllPostsRssFeed

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r"comments", CommentViewSet, basename="comment")

schema_view = get_schema_view(
    openapi.Info(
        title="测试工程API",
        default_version='v1.0',
        description="测试工程接口文档",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="xlivevil@aliyun.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('comments/', include('comments.urls')),
    path('accounts/', include('allauth.urls')),
    path('all/rss', AllPostsRssFeed(), name="rss"),
    path("api/", include(router.urls)),
    path("api/", include("api.urls")),
    path("api/auth/", include("rest_framework.urls",
                              namespace="rest_framework")),
    path('comments/', include('django_comments.urls')),
    # path('swagger(?P<format>/.json|/.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('todo/', include('todo.urls')),
    path('netdisk/', include('netdisk.urls')),
    path('wiki/', include('wiki.urls')),
    path('contact/', include('contact_form.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))
                   ] + urlpatterns
