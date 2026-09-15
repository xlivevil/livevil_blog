from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from djongo import models as mongomodels

from utils.rich_content import generate_rich_content


class Category(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


def change_category_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('category_updated_at', datetime.utcnow())


post_save.connect(receiver=change_category_updated_at, sender=Category)
post_delete.connect(receiver=change_category_updated_at, sender=Category)


class Tag(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


def change_tag_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('tag_updated_at', datetime.utcnow())


post_save.connect(receiver=change_tag_updated_at, sender=Tag)
post_delete.connect(receiver=change_tag_updated_at, sender=Tag)


class PostBody(mongomodels.Model):
    db_connection = 'mongodb'

    main = models.TextField(_('正文'))


class Post(models.Model):
    """

    """
    # 标题
    title = models.CharField(_('标题'), max_length=70)
    slug = models.SlugField(_('短网址'), unique=True, allow_unicode=True)

    # 正文
    body = models.TextField(_('正文'))
    # body_link = models.OneToOneField(PostBody,verbose_name='正文链接')

    # 时间信息 可以使用auto_now_add=True
    create_time = models.DateTimeField(_('创建时间'), default=timezone.now)
    modified_time = models.DateTimeField(_('修改时间'))

    # 摘要
    excerpt = models.CharField(_('摘要'), max_length=200, blank=True)

    # 分类关系和标签关系
    category = models.ForeignKey(Category, verbose_name=_('分类'), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_('标签'), blank=True)

    # 作者关系
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('作者'), on_delete=models.CASCADE)
    # 点赞数
    likes = models.PositiveIntegerField(_('获赞数'), default=0)

    is_hidden = models.BooleanField(verbose_name=_('隐藏'), default=False)

    is_top = models.BooleanField(verbose_name=_('置顶'), default=False)

    @property
    def toc(self):
        return self.rich_content.get('toc', '')

    @property
    def body_html(self):
        return self.rich_content.get('content', '')

    @cached_property
    def rich_content(self):
        ud = self.modified_time.strftime('%Y%m%d%H%M%S')
        md_key = f'post{self.id}_md_{ud}'
        cache_md = cache.get(md_key)
        if cache_md:
            rich_content = cache_md
        else:
            rich_content = generate_rich_content(self.body)
            cache.set(md_key, rich_content, 60 * 60 * 12)
        return rich_content

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        # 全量保存时才刷新时间戳/摘要/slug；指定字段保存（如点赞）时其余字段保持不动
        if update_fields is None or 'modified_time' in update_fields:
            self.modified_time = timezone.now()

            if not self.excerpt:
                body = self.rich_content.get('content', '')
                self.excerpt = strip_tags(body)[:200]

            if not self.slug:
                self.slug = self._get_unique_slug(slugify(self.title, allow_unicode=True)[:20])
            elif Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = self._get_unique_slug(self.slug)
        super().save(*args, **kwargs)

    def _get_unique_slug(self, base):
        # 逐个尝试候选值，避免并发或删除中间 slug 后产生唯一键冲突
        candidate, counter = base or 'post', 1
        while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            counter += 1
            candidate = f'{base}-{counter}'
        return candidate

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['-create_time']

    def __str__(self):
        return _('blog-') + self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    @property
    def view_num(self):
        return self.postviewinfo_set.count()


def change_post_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('post_updated_at', datetime.utcnow())


post_save.connect(receiver=change_post_updated_at, sender=Post)
post_delete.connect(receiver=change_post_updated_at, sender=Post)


class PostViewInfo(models.Model):

    post = models.ForeignKey(Post, verbose_name=_('文章'), on_delete=models.CASCADE)

    view_time = models.DateTimeField(_('浏览时间'), default=timezone.now)

    header = models.CharField(
        _('请求头'),
        max_length=200,
    )

    ip = models.GenericIPAddressField('IP',)

    class Meta:
        verbose_name = _('浏览记录')
        verbose_name_plural = _('浏览记录')
        ordering = ['-view_time']
