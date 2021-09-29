from django.apps import apps
from django.template import Context, Template
from django.test import TestCase

from blog.templatetags.blog_extra import show_recent_posts

from ..models import Category, Post


def test_show_recent_posts_with_posts(self):
    post = Post.objects.create(
        title='测试标题',
        body='测试内容',
        category=self.cate,
        author=self.user,
    )
    context = Context(show_recent_posts(self.ctx))
    template = Template('{% load blog_extras %}' '{% show_recent_posts %}')
    expected_html = template.render(context)
    self.assertInHTML('<h3 class="widget-title">最新文章</h3>', expected_html)
    self.assertInHTML(f'<a href="{post.get_absolute_url()}">{post.title}</a>', expected_html)
