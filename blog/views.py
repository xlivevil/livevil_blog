import json

from django.contrib import messages
from django.core.cache import cache
from django.db.models import Count, F, Q
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from pure_pagination import PaginationMixin

from blog.models import Category, Post, PostViewInfo, Tag
from utils.request import get_client_ip


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-create_time'
    context_object_name = 'post_list'
    # 内置分页器
    paginate_by = 5

    def get_queryset(self):
        # 预取关联并注解浏览量，避免列表页 N+1；distinct 防止后续 M2M 过滤导致计数翻倍
        return (
            super().get_queryset().filter(is_hidden=False).select_related('category', 'author').prefetch_related(
                'tags').annotate(view_num=Count('postviewinfo', distinct=True))
        )


class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('name'))
        return super().get_queryset().filter(category=cate).filter(is_hidden=False)


class ArchiveView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(create_time__year=year, create_time__month=month).filter(is_hidden=False)


class TagView(IndexView):

    def get_queryset(self):
        t = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return super().get_queryset().filter(tags=t).filter(is_hidden=False)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # 相邻文章只在已发布文章中取，各一条查询
        context['pre_article'] = Post.objects.filter(id__lt=self.object.id, is_hidden=False).order_by('-id').first()
        context['next_article'] = Post.objects.filter(id__gt=self.object.id, is_hidden=False).order_by('id').first()
        response = self.render_to_response(context)
        # 浏览记录：截断超长 UA，记录可信 IP（仅统计用途）
        header = (request.META.get('HTTP_USER_AGENT') or '')[:200]
        PostViewInfo.objects.create(post=self.object, header=header, ip=get_client_ip(request) or '0.0.0.0')
        return response


class IncreaseLikesView(View):

    def post(self, request, *args, **kwargs):
        if not request.accepts('application/json'):
            return HttpResponseBadRequest()
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()
        post = get_object_or_404(Post, pk=data.get('id'), is_hidden=False)
        # 服务端去重：登录用户按用户计数，匿名访客按可信 IP 计数，24 小时内只能点赞一次
        if request.user.is_authenticated:
            voter = f'user-{request.user.pk}'
        else:
            voter = f'ip-{get_client_ip(request) or "unknown"}'
        liked_key = f'blog:liked:{post.pk}:{voter}'
        if cache.get(liked_key):
            return JsonResponse({'status': 'ok', 'likes': post.likes, 'duplicate': True})
        # F 表达式原子自增：并发不丢更新，且不触发信号/全量 save
        Post.objects.filter(pk=post.pk).update(likes=F('likes') + 1)
        cache.set(liked_key, True, 60 * 60 * 24)
        post.refresh_from_db(fields=['likes'])
        return JsonResponse({'status': 'ok', 'likes': post.likes})


def search(request):
    """
    Search in posts

    Search by keyword, return list of post using template 'blog/index.html'
    """
    q = request.GET.get('q')

    if not q:
        error_msg = _('请输入搜索关键字')
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(is_hidden=False)
    return render(request, 'blog/index.html', {'post_list': post_list})


@cache_page(60 * 15)
def about(request):
    return render(request, 'blog/about.html')


class FullWidthView(IndexView):
    template_name = 'blog/full-width.html'


def blank(request):
    url = reverse('blog:index')
    return redirect(url)
