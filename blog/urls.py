from django.urls import include, path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'blog'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', views.blank),
    # path('contact', views.contact, name='contact'),
    path('full-width', views.FullWidthView.as_view(), name='full_width'),
    path('about', cache_page(60 * 60 * 23 + 646)(views.about), name='about'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('posts/<str:slug>', views.PostDetailView.as_view(), name='detail'),
    path('posts/archives/<int:year>/<int:month>', cache_page(60 * 15)(views.ArchiveView.as_view()), name='archive'),
    path('posts/tags/<str:name>', views.TagView.as_view(), name='tag'),
    path('posts/categories/<str:name>', views.CategoryView.as_view(), name='category'),
    path('increase-likes/', views.IncreaseLikesView.as_view(), name='increase_likes'),
    path('search/', include('haystack.urls')),
]
