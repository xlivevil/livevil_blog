from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, post_save
from djongo import models as mongomodels
from utils.rich_content import generate_rich_content


class Category(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('分类')
        verbose_name_plural = _('分类')

    def __str__(self):
        return self.name


def change_category_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("category_updated_at", datetime.utcnow())


post_save.connect(receiver=change_category_updated_at, sender=Category)
post_delete.connect(receiver=change_category_updated_at, sender=Category)


class Tag(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('标签')
        verbose_name_plural = _('标签')

    def __str__(self):
        return self.name


def change_tag_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("tag_updated_at", datetime.utcnow())


post_save.connect(receiver=change_tag_updated_at, sender=Category)
post_delete.connect(receiver=change_tag_updated_at, sender=Category)


class PostBody(mongomodels.Model):
    db_connection = 'mongodb'

    main = models.TextField(_('正文'))


class Post(models.Model):
    """

    """
    # TODO: 保存同时刷新缓存
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
    category = models.ForeignKey(Category,
                                 verbose_name=_('分类'),
                                 on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_('标签'), blank=True)

    # 作者关系
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('作者'),
                               on_delete=models.CASCADE)
    # 点赞数
    likes = models.PositiveIntegerField(_('获赞数'), default=0)

    is_hidden = models.BooleanField(verbose_name=_('隐藏'), default=False)

    is_top = models.BooleanField(verbose_name=_('置顶'), default=False)

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        ud = self.modified_time.strftime("%Y%m%d%H%M%S")
        md_key = 'post{}_md_{}'.format(self.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            rich_content = cache_md
        else:
            rich_content = generate_rich_content(self.body)
            cache.set(md_key, rich_content, 60 * 60 * 12)
        return rich_content

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.modified_time = timezone.now()

        if self.excerpt == '':
            body = self.rich_content.get("content", "")
            self.excerpt = strip_tags(body)[:200]

        if self.slug == '':
            slug = slugify(self.title, allow_unicode=True)[:20]
            if Post.objects.filter(slug=slug).exists():
                self.slug = "{}-{}".format(
                    slug,
                    Post.objects.filter(slug__startswith=slug).count() + 1)
            else:
                self.slug = slug

        super().save()

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['-create_time']

    def __str__(self):
        return "blog-" + self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # @property
    def view_num(self):
        # '浏览量'
        num = self.postviewinfo_set.count()
        return num
    view_num.short_description = _('浏览量')


def change_post_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("post_updated_at", datetime.utcnow())


post_save.connect(receiver=change_post_updated_at, sender=Post)
post_delete.connect(receiver=change_post_updated_at, sender=Post)


class PostViewInfo(models.Model):

    post = models.ForeignKey(Post, verbose_name=_('文章'), on_delete=models.CASCADE)

    view_time = models.DateTimeField(_('浏览时间'), default=timezone.now)

    header = models.CharField(
        _('请求头'),
        max_length=200,
    )

    ip = models.GenericIPAddressField('IP', )

    class Meta:
        verbose_name = _('浏览记录')
        verbose_name_plural = _('浏览记录')
        ordering = ['-view_time']
