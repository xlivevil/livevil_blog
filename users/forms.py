from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse

from users.models import User


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
