from django import template
from django.db.models import Count, Q

from blog.models import Category, Post, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.filter(is_hidden=False).order_by('-create_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.filter(is_hidden=False).dates('create_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_hidden=False))
    ).filter(num_posts__gt=0)

    return {'category_list': category_list}


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_hidden=False))
    ).filter(num_posts__gt=0).order_by('num_posts')
    return {'tag_list': tag_list}
