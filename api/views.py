from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from drf_yasg import openapi
from drf_yasg.inspectors import FilterInspector
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.fields import DateField
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_extensions.cache.decorators import cache_response

from api.filter import PostFilter
from api.permissions import IsSelfOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, PostHaystackSerializer, PostListSerializer, PostSerializer, TagSerializer,
    UserDetailSerializer, UserRegisterSerializer,
)
from blog.models import Category, Post, Tag
from comments.models import PostComment
from users.models import User

from .cache import (
    CategoryKeyConstructor, CommentListKeyConstructor, PostListKeyConstructor, PostObjectKeyConstructor,
    TagKeyConstructor,
)


class View(APIView):    # pragma: no cover

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
                obj = Post.objects.get(pk=pk, is_hidden=False)
                data = PostSerializer(obj).data
            except Exception as e:
                print(e)
                return Response({
                    'status': 404,
                    'msg': '没有找到',
                })
        else:
            query = Post.objects.filter(is_hidden=False).all()
            data = PostSerializer(query, many=True).data
        return Response({'status': 200, 'msg': 'ok', 'result': data})

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):    # 单增
            many = False
        elif isinstance(request_data, list):    # 群增
            many = True
        ser = PostSerializer(data=request_data)

        ser.is_valid()

        return Response('post OK')

    def delete(self, request, *args, **kwargs):
        pass


class IndexAPIView(ListModelMixin, GenericViewSet):    # pragma: no cover
    # 没有使用, 功能已整合进PostViewSet
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


# TODO: post category tags 都是传id 改为传字段
class PostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    PostViewSet

    list:
    list posts

    retrieve:
    get a post by id

    list_comments:
    get a post's comments

    list_archive_dates:
    list posts's archive dates
    """
    serializer_class = PostSerializer
    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostSerializer,
    }
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_class_table.get(self.action, super().get_serializer_class())

    # @cache_response(timeout=5 * 60, key_func=PostListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @cache_response(timeout=5 * 60, key_func=PostObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: _("归档日期列表，时间倒序排列。例如：['2020-08', '2020-06']。")})
    @action(
        methods=['GET'],
        detail=False,
        url_path='archive/dates',
        url_name='archive-date',
        filter_backends=[],
        pagination_class=None,
    )
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates('create_time', 'month', order='DESC')
        date_field = DateField(format='%Y-%m')
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=True,
        url_path='comments',
        url_name='comment',
        filter_backends=[],
        suffix='List',
        pagination_class=LimitOffsetPagination,
        serializer_class=CommentSerializer,
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论 self.object.content_object  self.object.pk
        content_type = ContentType.objects.get(app_label=post._meta.app_label, model=post._meta.model_name)
        queryset = PostComment.objects.filter(content_type=content_type, object_pk=post.pk).order_by('-created_time')
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


index = PostViewSet.as_view({'get': 'list'})


class CommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return PostComment.objects.all()

    # @cache_response(timeout=5 * 60, key_func=CommentListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostSearchAnonRateThrottle(AnonRateThrottle):
    """
    游客搜索频率限制
    """
    THROTTLE_RATES = {'anon': '5/min'}


class PostSearchUserRateThrottle(UserRateThrottle):
    """
    用户搜索频率限制
    """
    THROTTLE_RATES = {'user': '10/min'}


class PostSearchFilterInspector(FilterInspector):
    """
    swagger text 字段提示
    """

    def get_filter_parameters(self, filter_backend):
        return [
            openapi.Parameter(
                name='text',
                in_=openapi.IN_QUERY,
                required=True,
                description=_('搜索关键词'),
                type=openapi.TYPE_STRING,
            )
        ]


# @method_decorator(name='retrieve',
#                   decorator=swagger_auto_schema(auto_schema=None, ))
@method_decorator(name='list', decorator=swagger_auto_schema(filter_inspectors=[PostSearchFilterInspector]))
class PostSearchView(HaystackViewSet):
    """
    搜索视图集

    retrieve:
    search/42/?model=myapp.person
    返回

    list:
    search/?text=key
    返回搜索结果列表
    """

    index_models = [Post]
    serializer_class = PostHaystackSerializer
    throttle_classes = [PostSearchAnonRateThrottle, PostSearchUserRateThrottle]
    filter_backends = [HaystackAutocompleteFilter]


class TagViewSet(ListModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        return Tag.objects.all().order_by('name')

    @cache_response(timeout=5 * 60, key_func=TagKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.all().order_by('name')

    @cache_response(timeout=5 * 60, key_func=CategoryKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @action(detail=False)
    def sorted(self, request):
        users = User.objects.all().order_by('-username')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
