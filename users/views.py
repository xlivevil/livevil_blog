from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from users.forms import ProfileForm


@login_required  # 判断用户是否登录
def profile(request):
    """ 个人资料 """
    user = request.user
    return render(request, 'profile.html', {'user': user, })


@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_vaild():
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', context={'form': form})
