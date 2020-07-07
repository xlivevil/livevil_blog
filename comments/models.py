from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.querysets import TreeQuerySet

from utils.rich_content import generate_rich_content


class BlogCommentQuerySet(TreeQuerySet):

    def visible(self):
        return self.filter(is_public=True, is_removed=False)

    def roots(self):
        return self.visible().filter(parent__isnull=True)


class BlogCommentManager(TreeManager, CommentManager):
    pass


class PostComment(MPTTModel, CommentAbstractModel):
    # TODO: 加入点赞数

    # 时间信息
    created_time = models.DateTimeField(_('创建时间'), default=timezone.now)

    # 层级关系
    parent = TreeForeignKey('self', verbose_name=_('父评论'), null=True, blank=True,
                            on_delete=models.DO_NOTHING, related_name='children')

    objects = BlogCommentManager.from_queryset(BlogCommentQuerySet)()

    class Meta(CommentAbstractModel.Meta):
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        db_table = 'Blog_comments'

    class MPTTMeta:
        # 必须加入 user_id，否则在调用 mptt 的 get_queryset_descendants 时，
        # 确保 select_related user 时 user_id 字段已经 load，否则会报错：
        # Field %s.%s cannot be both deferred and traversed using select_related at the same time.
        order_insertion_by = ["-submit_date", "user_id"]

    def __str__(self):
        return f'{self.user}:{self.comment[:40]}'

    @property
    def comment_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        ud = self.submit_date.strftime("%Y%m%d%H%M%S")
        md_key = 'comment{}_md_{}'.format(self.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            rich_content = cache_md
        else:
            rich_content = generate_rich_content(self.comment)
            cache.set(md_key, rich_content, 60*60*12)
        return rich_content
