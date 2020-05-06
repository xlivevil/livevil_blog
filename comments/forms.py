from django import forms
from django.forms import Textarea

from comments.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body', ]
        widgets = {
            'body': Textarea(attrs={"style": "display:none;"})
        }
