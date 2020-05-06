from django.core.cache import cache
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.functional import cached_property

from blog.models import Post
from users.models import User
from utils.rich_content import generate_rich_content


class Comment(models.Model):
    # TODO: 加入点赞数，回复
    # 正文
    body = models.TextField('内容')

    # 时间信息
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 作者关系
    user = models.ForeignKey(User, verbose_name='评论者', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', verbose_name='父评论', null=True, blank=True, on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.modified_time = timezone.now()
        super().save()

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return '{}:{}'.format(self.user, self.body[:40])

#     def get_absolute_url(self):
#         return reverse('comments', kwargs={'post': self.post,})
    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        ud = self.modified_time.strftime("%Y%m%d%H%M%S")
        md_key = 'comment{}_md_{}'.format(self.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            rich_content = cache_md
        else:
            rich_content = generate_rich_content(self.body)
            cache.set(md_key, rich_content, 60*60*12)
        return rich_content
