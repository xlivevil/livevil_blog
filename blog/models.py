from django.contrib.contenttypes.fields import GenericRelation
from django.core.cache import cache
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags

from comments.models import PostComment
from users.models import User
from utils.rich_content import generate_rich_content


class Category(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """

    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """

    """
    # TODO: 保存同时刷新缓存
    # 标题
    title = models.CharField('标题', max_length=70)

    # 正文
    body = models.TextField('正文')

    # 时间信息
    create_time = models.DateTimeField('创建时间', default=timezone.now)    # 可以使用auto_now_add=True
    modified_time = models.DateTimeField('修改时间')

    # 摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 分类关系和标签关系
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 作者关系
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    is_hidden = models.BooleanField(verbose_name='隐藏', default=False)

    is_top = models.BooleanField(verbose_name='置顶', default=False)

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
            cache.set(md_key, rich_content, 60*60*12)
        return rich_content

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.modified_time = timezone.now()

        if self.excerpt == '':
            self.excerpt = strip_tags(self.rich_content.get("content", ""))[:200]
        super().save()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return "blog-"+self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    @property
    def get_view_num(self):
        # verbose_name = '浏览量'
        num = self.postviewinfo_set.count()
        return num


class PostViewInfo(models.Model):
    # TODO: 加入记录间隔
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE)

    view_time = models.DateTimeField('浏览时间', default=timezone.now)

    header = models.CharField('请求头', max_length=200,)

    ip = models.CharField('IP', max_length=30)

    class Meta:
        verbose_name = '浏览记录'
        verbose_name_plural = verbose_name
        ordering = ['-view_time']

