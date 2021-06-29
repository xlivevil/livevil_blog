from django.urls import path, include

from comments import views

app_name = 'comments'
urlpatterns = [
    path('', include('django_comments.urls')),
    path('reply/<int:parent>',
         views.ReplyView.as_view(),
         name='post_comments_reply'),
]
