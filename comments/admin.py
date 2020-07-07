from django.contrib import admin

# Register your models here.
from reversion.admin import VersionAdmin

from comments.models import PostComment


@admin.register(PostComment)
class CommentAdmin(VersionAdmin):
    # 排序
    date_hierarchy = 'created_time'
    # 显示列表显示项
    list_display = ('user', 'created_time', 'submit_date',)
    # 过滤器
    list_filter = ('user', 'created_time', 'submit_date', )
    #
    list_per_page = 20

    fields = ('user', 'created_time', 'submit_date', 'comment', 'parent', 'content_type',)
    # 分类排列
    # fieldsets =
    # 左右多选框
    # filter_horizontal = ('tags',)

    def get_queryset(self, request):
        # superuser 获得全部结果 其他用户获得自己的
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)