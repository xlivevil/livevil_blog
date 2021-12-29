from django.conf import settings
from django.utils import timezone

from ..models import PostComment
from .base import CommentDataTestCase


class PostCommentModelTestCase(CommentDataTestCase):

    def setUp(self):
        super().setUp()
        self.comment = PostComment.objects.create(
            user=self.user,
            user_email='a@a.com',
            comment='评论内容',
            content_type=self.post_content_type,
            object_pk=str(self.post.pk),
            site_id=getattr(settings, 'SITE_ID', None),
            submit_date=timezone.now()
        )

    def test_str_representation(self):
        self.assertEqual(self.comment.__str__(), 'admin: 评论内容...')

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.comment.modified_time)

        old_comment_modified_time = self.comment.modified_time
        self.comment.comment = '新的评论内容'
        self.comment.save()
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.modified_time > old_comment_modified_time)

    def test_subcomment(self):
        sub_comment = PostComment.objects.create(
            user=self.user,
            user_email='a@a.com',
            comment='子评论内容',
            content_type=self.post_content_type,
            object_pk=str(self.post.pk),
            site_id=getattr(settings, 'SITE_ID', None),
            parent=self.comment,
            submit_date=timezone.now()
        )
        self.assertEqual(sub_comment.parent, self.comment)
        self.assertEqual(self.comment.children.count(), 1)
