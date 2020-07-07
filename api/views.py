from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.fields import DateField
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.filter import PostFilter
from api.serializers import PostSerializer, CommentSerializer
from blog.models import Post
from comments.models import PostComment


class View(APIView):

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                obj = Post.objects.get(pk=pk, is_delete=False)
                data = PostSerializer(obj).data
            except:
                return Response({
                    'status': 404,
                    'msg': '没有找到',
                })
        else:
            query = Post.objects.filter(is_delete=False).all()
            data = PostSerializer(query, many=True).data
        return Response({
            'status': 200,
            'msg': 'ok',
            'result': data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):  # 单增
            many = False
        elif isinstance(request_data, list):    # 群增
            many = True
        ser = PostSerializer(data=request_data)

        ser.is_valid()

        return Response('post OK')

    def delete(self, request, *args, **kwargs):
        pass


class IndexAPIView(ListModelMixin, GenericViewSet):
    # TODO: CURD全完成,认证模块完成
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class PostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    @action(
        methods=["GET"], detail=False, url_path="archive/dates", url_name="archive-date"
    )
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates("create_time", "month", order="DESC")
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
            methods=["GET"],
            detail=True,
            url_path="comments",
            url_name="comment",
            pagination_class=LimitOffsetPagination,
            serializer_class=CommentSerializer,
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论 self.object.content_object  self.object.pk
        content_type = ContentType.objects.get(app_label=post._meta.app_label, model=post._meta.model_name)
        queryset = PostComment.objects.filter(content_type=content_type, object_pk=post.pk).order_by("-created_time")
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


class CommentViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return PostComment.objects.all()
