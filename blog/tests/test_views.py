import json
from datetime import timedelta

from django.apps import apps
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.feed import AllPostsRssFeed
from users.models import User

from blog.models import Category, Post, Tag


class BlogDataTestCase(TestCase):

    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()

        # User
        self.user = User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')

        # 分类
        self.cate1 = Category.objects.create(name='测试分类一')
        self.cate2 = Category.objects.create(name='测试分类二')

        # 标签
        self.tag1 = Tag.objects.create(name='测试标签一')
        self.tag2 = Tag.objects.create(name='测试标签二')

        # 文章
        self.post1 = Post.objects.create(
            title='测试标题一',
            body='测试内容一',
            category=self.cate1,
            author=self.user,
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='测试标题二',
            body='测试内容二',
            category=self.cate2,
            author=self.user,
            create_time=timezone.now() - timedelta(days=100)
        )


class CategoryViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('blog:category', kwargs={'name': self.cate1.name})
        self.url2 = reverse('blog:category', kwargs={'name': self.cate2.name})

    def test_visit_a_nonexistent_category(self):
        url = reverse('blog:category', kwargs={'name': 'XX'})
        response = self.client.get(url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, '暂时还没有文章')

    def test_with_posts(self):
        response = self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.cate1.post_set.all().order_by('-create_time')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class ArchiveViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse(
            'blog:archive', kwargs={
                'year': self.post1.create_time.year,
                'month': self.post1.create_time.month
            }
        )

    def test_visit_archive_without_any_post(self):
        Post.objects.all().delete()
        cache.clear()
        response = self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, '暂时还没有文章')

    def test_visit_archive_with_posts(self):
        cache.clear()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        now = timezone.now()
        expected_qs = Post.objects.filter(create_time__year=now.year, create_time__month=now.month)
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class TagViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('blog:tag', kwargs={'name': self.tag1.name})
        self.url2 = reverse('blog:tag', kwargs={'name': self.tag2.name})

    def test_visit_a_nonexistent_tag(self):
        url = reverse('blog:tag', kwargs={'name': 'XX'})
        response = self.client.get(url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, '暂时还没有文章')

    def test_with_posts(self):
        response = self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.tag1.post_set.all().order_by('-create_time')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class IncreaseLikesViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('blog:increase_likes')

    def test_increaselikes(self):
        dict_data = {'object': 'post', 'id': self.post1.pk}
        data = json.dumps(dict_data)
        response = self.client.post(
            self.url, data=data, content_type='application/json', HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.likes, 1)


class PostDetailViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.md_post = Post.objects.create(
            title='Markdown 测试标题',
            body='# 标题',
            category=self.cate1,
            author=self.user,
        )
        self.url = reverse('blog:detail', kwargs={'pk': self.md_post.pk})

    def test_good_view(self):
        response = self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/detail.html')
        self.assertContains(response, self.md_post.title)
        self.assertIn('post', response.context)

    def test_visit_a_nonexistent_post(self):
        url = reverse('blog:detail', kwargs={'pk': 100})
        response = self.client.get(url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 404)

    def test_view_num(self):
        self._view_and_get_view_num(1)
        self._view_and_get_view_num(2)

    def _view_and_get_view_num(self, arg):
        self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.view_num, arg)

    def test_markdownify_post_body_and_set_toc(self):
        response = self.client.get(self.url, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertContains(response, '文章目录')
        self.assertContains(response, self.md_post.title)

        post_template_var = response.context['post']
        self.assertHTMLEqual(post_template_var.body_html, "<h1 id='标题'>标题</h1>")
        self.assertHTMLEqual(post_template_var.toc, '<li><a href="#标题">标题</li>')


class AdminTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.test_user = User.objects.create_superuser(username='test', email='test@test.com', password='test')
        self.url = reverse('admin:blog_post_add')
        self.url2 = reverse('admin:blog_post_change', args=(self.post1.pk,))
        self.url3 = reverse('admin:blog_post_changelist')

    def test_set_author_after_publishing_the_post(self):
        data = {'title': '测试标题', 'body': '测试内容', 'category': self.cate1.pk, 'slug': '测试'}
        self.client.login(username=self.user.username, password='admin')
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.all().latest('create_time')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, data.get('title'))
        self.assertEqual(post.category, self.cate1)

    def test_Permissions(self):
        data = {'title': '权限测试标题', 'body': '权限测试内容', 'category': self.cate1.pk, 'slug': '权限测试'}
        self.client.login(username=self.user.username, password='admin')
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        data = {'title': '普通权限测试标题', 'body': '普通同权限测试内容', 'category': self.cate1.pk, 'slug': '权限测试'}
        self.client.login(username=self.test_user.username, password='admin')
        test_response = self.client.post(self.url, data=data)
        self.assertEqual(test_response.status_code, 200)

    def test_change_post(self):
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.body)
        self.assertContains(response, self.post1.category.name)
    
    def test_change_list(self):
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(self.url3)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.category.name)
        self.assertContains(response, f'<td class="field-postview_count">{self.post1.postviewinfo_set.count()}</td>')

class RSSTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('rss')

    def test_rss_subscription_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, AllPostsRssFeed.title)
        self.assertContains(response, AllPostsRssFeed.description)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)
        self.assertContains(response, f'[{self.post1.category}] {self.post1.title}')
        self.assertContains(response, f'[{self.post2.category}] {self.post2.title}')
        self.assertContains(response, self.post1.body)
        self.assertContains(response, self.post2.body)


