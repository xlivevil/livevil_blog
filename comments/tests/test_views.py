from django.conf import settings
from django.urls import reverse

from ..models import PostComment
from .base import CommentDataTestCase


class PostCommentViewTestCase(CommentDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('comments:comments-post-comment')
