from django.urls import path
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import DefaultRouter

from . import views
from .views import PostViewSet


app_name = 'api'
urlpatterns = [
    # path('index', views.IndexAPIView.as_view(), name='indexAPI'),

]