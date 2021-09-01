from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views

app_name = 'blog'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', views.blank),
    # path('contact', views.contact, name='contact'),
    path('full-width', views.FullWidthView.as_view(), name='full_width'),
    path('about', cache_page()(views.about), name='about'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('posts/<str:slug>', views.PostDetailView.as_view(), name='detail'),
    path('posts/archives/<int:year>/<int:month>',
         cache_page(60 * 15)(views.ArchiveView.as_view()),
         name='archive'),
    path('posts/tags/<str:name>', views.TagView.as_view(), name='tag'),
    path('posts/categories/<str:name>',
         views.CategoryView.as_view(),
         name='category'),
    path('search/', include('haystack.urls')),
]

# handler404 = views.page_not_found
# handler500 = views.page_error
