from django.apps import apps
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Post
from blog.search_indexes import NoteIndex
from users.models import User


class PostModelTestCase(TestCase):

    def setUp(self):
        # 断开 haystack 的 signal，测试生成的文章无需生成索引
        apps.get_app_config('haystack').signal_processor.teardown()
        user = User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), 'blog-' + self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = '新的测试内容'
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 200)

    def test_auto_populate_slug(self):
        self.assertIsNotNone(self.post.slug)
        self.assertTrue(0 < len(self.post.slug) <= 20)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_duplicate_slug(self):
        self.post2 = Post.objects.create(
            title=self.post.title,
            body=self.post.body,
            category=self.post.category,
            author=self.post.author,
        )


class SearchIndexesTestCase(TestCase):

    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()
        user = User.objects.create_superuser(username='admin', email='admin@hellogithub.com', password='admin')
        cate = Category.objects.create(name='测试')
        Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )
        another_cate = Category.objects.create(name='另一个测试')
        Post.objects.create(
            title='另一个测试标题',
            body='另一个测试内容',
            category=another_cate,
            author=user,
        )
        self.index_instance = NoteIndex()

    def test_get_model(self):
        self.assertTrue(issubclass(self.index_instance.get_model(), Post))

    def test_index_queryset(self):
        expected_qs = Post.objects.all()
        self.assertQuerysetEqual(self.index_instance.index_queryset(), [repr(p) for p in expected_qs])
