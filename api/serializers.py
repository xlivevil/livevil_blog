from django.utils.translation import gettext_lazy as _
from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from rest_framework.fields import CharField

from blog.highlighter import Highlighter
from blog.models import Category, Post, Tag
from comments.models import PostComment
from users.models import User


class CategorySerializer(serializers.ModelSerializer[Category]):

    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer[Tag]):

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class UserSerializer(serializers.ModelSerializer[User]):

    class Meta:
        model = User
        fields = ['id', 'username']


class PostListSerializer(serializers.ModelSerializer[Post]):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'create_time',
            'excerpt',
            'category',
            'tags',
            'author',
            'view_num',
        ]


class PostSerializer(serializers.ModelSerializer[Post]):
    category = CategorySerializer()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    toc = serializers.CharField(label=_('文章目录'))
    body_html = serializers.CharField(label=_('文章内容'))

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'body',
            'category',
            'author',
            'create_time',
            'modified_time',
            'tags',
            'toc',
            'body_html',
            'view_num',
        ]

        read_only_fields = [
            'id',
            'create_time',
            'modified_time',
            'toc',
            'body_html',
            'get_view_num',
        ]
        extra_kwargs = {
            'rich_content': {
                'body_html': True
            },
            'toc': {
                'body_html': True
            },
        }


class UserRegisterSerializer(serializers.ModelSerializer[User]):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'last_login', 'date_joined']


class CommentSerializer(serializers.ModelSerializer[PostComment]):

    class Meta:
        model = PostComment
        fields = [
            'user_id', 'user_name', 'user_email', 'user_url', 'comment', 'created_time', 'parent', 'content_type',
            'object_pk', 'comment_html'
        ]
        read_only_fields = ['created_time', 'comment_html']
        extra_kwargs = {'post': {'write_only': True}}


class HighlightedCharField(CharField):

    def to_representation(self, value):
        value = super().to_representation(value)
        request = self.context['request']
        query = request.query_params['text']
        highlighter = Highlighter(query)
        return highlighter.highlight(value)


class PostHaystackSerializer(HaystackSerializerMixin, PostListSerializer):
    title = HighlightedCharField(label='标题', help_text='标题中包含的关键词已由 HTML 标签包裹，并添加了 class，前端可设置相应的样式来高亮关键。')
    summary = HighlightedCharField(
        source='body',
        label='摘要',
        help_text='摘要中包含的关键词已由 HTML 标签包裹，并添加了 class，前端可设置相应的样式来高亮关键。',
    )

    class Meta(PostListSerializer.Meta):
        search_fields = ['text']
        fields = ['id', 'title', 'create_time', 'excerpt', 'category', 'author', 'view_num', 'summary']
