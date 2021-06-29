from django.conf import settings
from django.utils import timezone
from .base import CommentDataTestCase
from ..models import PostComment


class PostCommentModelTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.comment = PostComment.objects.create(
            user=self.user,
            user_email='a@a.com',
            comment='评论内容',
            content_type=self.post_content_type,
            object_pk=str(self.post.pk),
            site_id=getattr(settings, "SITE_ID", None),
            submit_date=timezone.now()
        )

    def test_str_representation(self):
        self.assertEqual(self.comment.__str__(), 'admin: 评论内容')

# TODO：测试子评论