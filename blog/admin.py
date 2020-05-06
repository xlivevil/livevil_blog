from django.contrib import admin

# Register your models here.
from reversion.admin import VersionAdmin

from blog.models import Post, Category, Tag, PostViewInfo


@admin.register(Post)
class PostAdmin(VersionAdmin):
    # 排序
    date_hierarchy = 'create_time'
    # 显示列表显示项
    list_display = ('title', 'create_time', 'modified_time', 'category', 'author', 'get_view_num')
    # 过滤器
    list_filter = ('create_time', 'category', 'tags',)
    #
    list_per_page = 20

    fields = ('title', 'body', 'excerpt', 'category', 'tags', 'is_hidden', 'is_top')
    # 分类排列
    # fieldsets =
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


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


admin.site.register(Category)
admin.site.register(Tag)
admin.site.site_header = '网站管理'
admin.site.site_title = '后台管理'
# TODO: 修改后台admin视图、模板、方法、
