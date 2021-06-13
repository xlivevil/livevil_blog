from django.contrib import admin

# Register your models here.
from reversion.admin import VersionAdmin

from users.models import User


@admin.register(User)
class UserAdmin(VersionAdmin):
    # 排序
    date_hierarchy = 'create_time'
    # 显示列表显示项
    list_display = ('username', 'nickname', 'create_time', 'email')
    # 过滤器
    list_filter = ('create_time', )
    #
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
