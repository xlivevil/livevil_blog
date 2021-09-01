from django.contrib import messages
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from pure_pagination import PaginationMixin

from blog.models import Post, Category, Tag, PostViewInfo


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'index.html'
    ordering = '-create_time'
    context_object_name = 'post_list'
    # 内置分页器
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(is_hidden=False)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('name'))
        return super().get_queryset().filter(category=cate).filter(
            is_hidden=False)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(
            create_time__year=year,
            create_time__month=month).filter(is_hidden=False)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return super().get_queryset().filter(tags=t).filter(is_hidden=False)


class PostDetailView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 重写get方法
        # 阅读数增加操作
        if kwargs.get('pk'):
            post_id = kwargs['pk']
        if kwargs.get('slug'):
            post_slug = kwargs['slug']
            post_id = Post.objects.filter(slug=post_slug).first().pk
        header = request.META.get('HTTP_USER_AGENT')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            ip = request.META.get('REMOTE_ADDR')

        post_view = PostViewInfo(post_id=post_id, header=header, ip=ip)
        post_view.save()
        return response


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs.get('id'))
        post.likes += 1
        post.save()
        return HttpResponse('success')


def search(request):
    """
    Search in posts

    Search by keyword, return list of post using template 'index.html'
    """
    q = request.GET.get('q')

    if not q:
        error_msg = _('请输入搜索关键字')
        messages.add_message(request,
                             messages.ERROR,
                             error_msg,
                             extra_tags='danger')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q)).filter(is_hidden=False)
    return render(request, 'index.html', {'post_list': post_list})


@cache_page(60 * 15)
def about(request):
    return render(request, 'about.html')


class FullWidthView(IndexView):
    template_name = 'full-width.html'


def blank(request):
    url = reverse('blog:index')
    return redirect(url)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def page_error(request, exception):
    return render(request, '404.html', status=500)
