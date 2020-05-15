from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
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
        return super().get_queryset().filter(category=cate).filter(is_hidden=False)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(create_time__year=year,
                                             create_time__month=month).filter(is_hidden=False)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return super().get_queryset().filter(tags=t).filter(is_hidden=False)


@cache_page(60*15)
def contact(request):
    return render(request, 'contact.html')


class PostDetailView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 重写get方法
        # 阅读数增加操作
        post_id = kwargs['pk']
        header = request.META.get('HTTP_USER_AGENT')
        ip = request.META.get('REMOTE_ADDR')
        # print(request.environ)
        # print(ip)
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        post_view = PostViewInfo(post_id=post_id, header=header, ip=ip)
        post_view.save()
        return response


# class SearchView(IndexView):
#     def get_queryset(self):
#         search = self.kwargs.get('q')
#
#         if not search:
#             error_msg = "请的输入搜索关键词"
#             messages.add_message(request,)

def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = '请输入搜索关键字'
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')  # 以后改为跳转至前一页

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(is_hidden=False)
    return render(request, 'index.html', {'post_list': post_list})


@cache_page(60*15)
def about(request):
    return render(request, 'about.html')


def full_width(request):
    return render(request, 'full-width.html')


def blank(request):
    url = reverse('blog:index')
    return redirect(url)


