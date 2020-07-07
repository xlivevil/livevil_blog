from rest_framework import serializers

from blog.models import Category, Tag, Post
from comments.models import PostComment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username"
        ]


class PostSerializer(serializers.ModelSerializer):
    # TODO: 整合序列化反序列化
    category = CategorySerializer()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    toc = serializers.CharField()
    body_html = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "author",
            "excerpt",
            "tags",
            "toc",
            "body_html",
        ]
        extra_kwargs = {
            "id": {
                'read_only': True
            },
            "rich_content": {
                'body_html': True
            },
            "toc": {
                'body_html': True
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = [
            "user_id",
            "user_name",
            "user_email",
            "user_url",
            "comment",
            "created_time",
            "parent",
            "content_type",
            "object_pk"
        ]
        read_only_fields = [
            "created_time",
        ]
        extra_kwargs = {"post": {"write_only": True}}
