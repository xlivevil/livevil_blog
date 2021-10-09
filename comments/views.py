from django.contrib import messages
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_comments.forms import CommentForm
from django_comments.signals import comment_was_posted
from notifications.signals import notify

from blog.models import Post
from comments.forms import PostCommentForm
from comments.models import PostComment


@require_POST
def comment_preview(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
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


@receiver(comment_was_posted)
def comment_notice(sender, **kwargs):
    comment = kwargs.pop('comment')
    request = kwargs.pop('request')
    if comment.parent:

        notify.send(
            request.user,
            recipient=comment.parent.user,
            verb='回复了你',
            target=comment.content_object,
            action_object=comment,
            description=comment.comment[:40]
        )

    notify.send(
        request.user,
        recipient=comment.content_object.author,
        verb='回复了你',
        target=comment.content_object,
        action_object=comment,
        description=comment.comment[:40]
    )


class ReplyView(FormMixin, DetailView):
    model = PostComment
    form_class = PostCommentForm
    pk_url_kwarg = 'parent'
    template_name = 'comments/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'target_object': self.object.content_object,
                'parent': self.object.pk,
                'user': self.request.user
            }
        )
        return kwargs
