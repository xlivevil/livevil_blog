from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_comments.forms import CommentForm

from comments import get_model


class PostCommentForm(CommentForm):

    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    SPAM_MESSAGE = _('Your message was classified as spam.')

    def __init__(self, target_object, data=None, initial=None, parent=None, **kwargs):
        self.user = kwargs.pop('user', None)
        self.parent = parent
        self.request = kwargs.pop('request', None)
        # ReplyView 会传入这两个参数；渲染阶段用不到，弹出以避免传入 CommentForm 时报 TypeError
        self.user_ip = kwargs.pop('user_ip', None)
        self.user_agent = kwargs.pop('user_agent', None)
        if initial is None:
            initial = {}
        if parent:
            initial.update({'parent': self.parent})
        super().__init__(target_object, data=data, initial=initial, **kwargs)

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, **kwargs):
        data = super().get_comment_create_data(**kwargs)
        parent = self.cleaned_data.get('parent')
        data['parent_id'] = parent
        return data

    def clean_comment(self) -> str:
        from akismet import Akismet

        akismet_api = Akismet(
            key=getattr(settings, 'AKISMET_API_KEY', None),
            blog_url=getattr(settings, 'AKISMET_BLOG_URL', None),
        )
        akismet_kwargs = {
            'user_ip': self.data['user_ip'],
            'user_agent': self.data['user_agent'],
            'comment_author': self.cleaned_data.get('name'),
            'comment_author_email': self.cleaned_data.get('email'),
            'comment_content': self.cleaned_data['comment'],
            'comment_type': 'comment',
        }
        if akismet_api.comment_check(**akismet_kwargs):
            raise forms.ValidationError(self.SPAM_MESSAGE)
        return super().clean_comment()
