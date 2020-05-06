from django import template

from comments.forms import CommentForm

register = template.Library()


@register.inclusion_tag('inclusions/_comment_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
        return {
            'form': form,
            'post': post,
        }


@register.inclusion_tag('inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-create_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
