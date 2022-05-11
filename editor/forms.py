from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import Test


class CreationTestForm(ModelForm):
    icon = forms.ImageField()

    class Meta:
        model = Test
        fields = ('name', 'description', 'icon')
