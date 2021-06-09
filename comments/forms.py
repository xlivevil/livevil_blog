from django import forms
from django_comments.forms import CommentForm

from comments import get_model


class PostCommentForm(CommentForm):

    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self,
                 target_object,
                 data=None,
                 initial=None,
                 parent=None,
                 **kwargs):
        self.user = kwargs.pop('user', None)
        self.parent = parent
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
