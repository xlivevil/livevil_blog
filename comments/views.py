from django import apps
from django.apps import apps
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.utils.http import escape_leading_slashes
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_comments import signals
from django_comments.forms import CommentForm
from django_comments.signals import comment_was_posted
from django_comments.views.comments import CommentPostBadRequest
from django_comments.views.utils import next_redirect
from notifications.signals import notify

from blog.models import Post
from comments import get_form
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
    if comment.parent and request.user != comment.parent.user:

        notify.send(
            request.user,
            recipient=comment.parent.user,
            verb='回复了你',
            target=comment.content_object,
            action_object=comment,
            description=comment.comment[:40]
        )
    if request.user != comment.content_object.author:
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
        user_ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT')
        kwargs.update(
            {
                'target_object': self.object.content_object,
                'parent': self.object.pk,
                'user': self.request.user,
                'user_ip': user_ip,
                'user_agent': user_agent,
            }
        )

        return kwargs


@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()

    data['user_ip'] = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    data['user_agent'] = request.META.get('HTTP_USER_AGENT')

    if request.user.is_authenticated:
        if not data.get('name', ''):
            data['name'] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data['email'] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get('content_type')
    object_pk = data.get('object_pk')
    if ctype is None or object_pk is None:
        return CommentPostBadRequest('Missing content_type or object_pk field.')
    try:
        model = apps.get_model(*ctype.split('.', 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest('Invalid content_type value: %r' % escape_leading_slashes(ctype))
    except AttributeError:
        return CommentPostBadRequest('The given content-type %r does not resolve to a valid model.' % escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            f'No object matching content-type {escape(ctype)!r} and object PK {escape(object_pk)!r} exists.'
        )
    except (ValueError, ValidationError) as e:
        return CommentPostBadRequest(
            'Attempting to get content-type {!r} and object PK {!r} raised {}'.format(
                escape(ctype), escape(object_pk), e.__class__.__name__
            )
        )

    # Do we want to preview the comment?
    preview = 'preview' in data

    # Construct the comment form
    form = get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            'The comment form failed security verification: %s' % escape(str(form.security_errors()))
        )

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
        # These first two exist for purely historical reasons.
        # Django v1.0 and v1.1 allowed the underscore format for
        # preview templates, so we have to preserve that format.
            f'comments/{model._meta.app_label}_{model._meta.model_name}_preview.html',
            'comments/%s_preview.html' % model._meta.app_label,
        # Now the usual directory based template hierarchy.
            f'comments/{model._meta.app_label}/{model._meta.model_name}/preview.html',
            'comments/%s/preview.html' % model._meta.app_label,
            'comments/preview.html',
        ]
        return render(
            request,
            template_list,
            {
                'comment': form.data.get('comment', ''),
                'form': form,
                'next': data.get('next', next),
            },
        )

    # Otherwise create the comment
    comment = form.get_comment_object(site_id=get_current_site(request).id)
    comment.ip_address = request.META.get('REMOTE_ADDR', None) or None
    if request.user.is_authenticated:
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(sender=comment.__class__, comment=comment, request=request)

    for (receiver, response) in responses:
        if response is False:
            return CommentPostBadRequest('comment_will_be_posted receiver %r killed the comment' % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(sender=comment.__class__, comment=comment, request=request)

    return next_redirect(request, fallback=next or 'comments-comment-done', c=comment._get_pk_val())
