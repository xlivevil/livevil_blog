from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogCommentsConfig(AppConfig):
    name = 'comments'
    verbose_name = _('评论')
