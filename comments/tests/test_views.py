from django.conf import settings
from django.urls import reverse

from .base import CommentDataTestCase
from ..models import PostComment


class PostCommentViewTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('comments:comments-post-comment')
    # TODO：测试视图
