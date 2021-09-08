from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin

from blog.models import Category, Post, PostBody, PostViewInfo, Tag


@admin.register(Post)
class PostAdmin(VersionAdmin):
    # 排序
    date_hierarchy = 'create_time'
    # 显示列表显示项
    list_display = ('title', 'create_time', 'modified_time', 'category',
                    'author', 'postview_count', 'likes')
    # 过滤器
    list_filter = (
        'create_time',
        'category',
        'tags',
    )
    # 每页显示
    list_per_page = 20

    fields = ('title', 'slug', 'body', 'excerpt', 'category', 'tags',
              'is_hidden', 'is_top')
    # 分类排列
    # fieldsets =
    filter_horizontal = ('tags', )

    def save_model(self, request, obj, form, change):
        obj.author = request.user

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(_postview_count=Count('postviewinfo'), )
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    @admin.display(
        ordering='_postview_count',
        description=_('浏览量'),
    )
    def postview_count(self, obj):
        return obj._postview_count

    # postview_count.admin_order_field = '_postview_count'
    # postview_count.short_description = _('浏览量')


@admin.register(PostViewInfo)
class ViewInfoAdmin(VersionAdmin):
    # 排序
    date_hierarchy = 'view_time'
    # 显示列表显示项
    list_display = ('post', 'view_time', 'header', 'ip')
    # 过滤器
    list_filter = ('post', 'view_time', 'header', 'ip')
    #
    list_per_page = 20

    fields = ('post', 'view_time', 'header', 'ip')
    # 分类排列


admin.site.register(PostBody)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.site_header = 'Xlivevil后台'
admin.site.site_title = 'Xlivevil后台管理'
admin.site.index_title = '网站管理'
# TODO: 修改后台admin视图、模板、方法、
