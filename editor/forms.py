from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import Test


class CreationTestForm(ModelForm):
    project_name = forms.TextInput()
    description = forms.Textarea()
    icon = forms.ImageField()

    class Meta:
        model = Test
        fields = ('project_name', 'description', 'icon')


class EditTestInfo(ModelForm):
    name = forms.TextInput()
    description = forms.Textarea()
    icon = forms.ImageField()

    class Meta:
        model = Test
        fields = ('name', 'description', 'icon')
