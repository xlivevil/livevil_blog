from blog.highlighter import Highlighter
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from blog.models import Category, Tag, Post
from comments.models import PostComment
from rest_framework.fields import CharField
from drf_haystack.serializers import HaystackSerializerMixin
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
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
            'author',
            'get_view_num',
        ]


class PostSerializer(serializers.ModelSerializer):
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
            'get_view_num',
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

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def update(self, instance, validated_data):
    #     return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = [
            'user_id', 'user_name', 'user_email', 'user_url', 'comment',
            'created_time', 'parent', 'content_type', 'object_pk',
            'comment_html'
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
    title = HighlightedCharField(
        label='标题',
        help_text='标题中包含的关键词已由 HTML 标签包裹，并添加了 class，前端可设置相应的样式来高亮关键。')
    summary = HighlightedCharField(
        source='body',
        label='摘要',
        help_text='摘要中包含的关键词已由 HTML 标签包裹，并添加了 class，前端可设置相应的样式来高亮关键。',
    )

    class Meta(PostListSerializer.Meta):
        search_fields = ['text']
        fields = [
            'id', 'title', 'create_time', 'excerpt', 'category', 'author',
            'get_view_num', 'summary'
        ]
