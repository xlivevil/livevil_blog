from django.urls import include, path

from comments.views import ReplyView

app_name = 'comments'
urlpatterns = [
    # path('', include('django_comments.urls')),
    # path('post/', post_comment_notice, name='post-comment'),
    path('reply/<int:parent>', ReplyView.as_view(), name='post_comments_reply'),
]
