from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST

from blog.models import Post
from comments.forms import CommentForm


@require_POST
def comment_preview(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    # print(request.POST)
    # print(form)
    # print(post)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论成功！', extra_tags='success')
        return redirect(post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'preview.html', context=context)
