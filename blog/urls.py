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
from django.views.decorators.cache import cache_page

from . import views

app_name = 'blog'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', views.blank),
    path('contact', views.contact, name='contact'),
    path('full-width', views.FullWidthView.as_view(), name='full_width'),
    path('about', views.about, name='about'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('posts/archives/<int:year>/<int:month>', cache_page(60*15)(views.ArchiveView.as_view()), name='archive'),
    path('posts/tags/<str:name>', views.TagView.as_view(), name='tag'),
    path('posts/categories/<str:name>', views.CategoryView.as_view(), name='category'),
    path('search/', include('haystack.urls')),


]
