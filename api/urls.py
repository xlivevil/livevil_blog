from django.urls import include, path
from django.urls.conf import re_path
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import DefaultRouter
from api.views import (CategoryViewSet, CommentViewSet, PostSearchView,
                       PostViewSet, TagViewSet)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"search", PostSearchView, basename="search")

schema_view = get_schema_view(
    openapi.Info(
        title=_("测试工程API"),
        default_version='v1.0',
        description=_("测试工程接口文档"),
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="xlivevil@aliyun.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser, ),
)

app_name = 'api'
urlpatterns = [
    path('auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    re_path('swagger(?P<format>\.json|\.yaml)',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
