from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from blog.models import Post
from comments.forms import CommentForm, PostCommentForm
from comments.models import PostComment


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
    else:
        print(form)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'preview.html', context=context)


class ReplyView(FormMixin, DetailView):
    model = PostComment
    form_class = PostCommentForm
    pk_url_kwarg = 'parent'
    template_name = 'comments/form.html'

    def get_form_kwargs(self):
        kwargs = super(ReplyView, self).get_form_kwargs()
        kwargs.update({
            'target_object': self.object.content_object,
            'parent': self.object.pk,
            'user': self.request.user
        })
        return kwargs
