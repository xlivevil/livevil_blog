from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(LoginRequiredMixin, View):
    """更新通知状态

    修改状态的操作只接受 POST：GET 链接会被浏览器预取/爬虫误触发。
    """

    def post(self, request):
        notice_id = request.POST.get('notice_id')
        # 更新单条通知
        if notice_id:
            notice = get_object_or_404(request.user.notifications.all(), id=notice_id)
            notice.mark_as_read()
            return redirect(notice.target)
        # 更新全部通知
        request.user.notifications.mark_all_as_read()
        return redirect('notice:list')
