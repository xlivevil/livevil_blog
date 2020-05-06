from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-create_time')[:num],
    }


@register.inclusion_tag('inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('create_time', 'month', order="DESC")
    }


@register.inclusion_tag('inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # for cate in category_list:
    #     print(cate.num_posts)
    return {
        'category_list': category_list
    }


@register.inclusion_tag('inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0).order_by('num_posts')
    return {
        'tag_list': tag_list
    }

