from django.shortcuts import render

# Create your views here.
from rest_framework import response
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
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

from api.serializers import PostSerializer
from blog.models import Post


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


