from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import Test, Task


class CreationTestForm(ModelForm):
    project_name = forms.CharField(max_length=100)
    description = forms.Textarea()
    icon = forms.ImageField()

    # class Meta:
    #     model = Test
    #     fields = ('project_name', 'description', 'icon')


class EditTestInfo(ModelForm):
    name = forms.TextInput()
    description = forms.Textarea()
    icon = forms.ImageField()

    # class Meta:
    #     model = Test
    #     fields = ('name', 'description', 'icon')


class CreationTaskForm(ModelForm):
    name = forms.CharField(max_length=50)

    # class Meta:
    #     model = Task
    #     fields = ('name',)


class EditTaskInfo(ModelForm):
    pass
    # class Meta:
    #     model = Task
    #     fields = ('name', 'title')
