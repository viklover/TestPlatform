from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import Project, ProjectTask, ProjectExercise


class CreationProjectForm(ModelForm):
    project_name = forms.CharField(max_length=100)
    description = forms.Textarea()
    icon = forms.ImageField()

    class Meta:
        model = Project
        fields = ('project_name', 'description', 'icon')


class EditProjectInfo(ModelForm):
    name = forms.TextInput()
    description = forms.Textarea()
    icon = forms.ImageField()

    class Meta:
        model = Project
        fields = ('name', 'description', 'icon')


class CreationTaskForm(ModelForm):
    name = forms.CharField(max_length=50)

    class Meta:
        model = ProjectTask
        fields = ('name',)


class EditTaskInfo(ModelForm):
    pass

    class Meta:
        model = ProjectTask
        fields = ('name', 'title')


class CreationExerciseForm(ModelForm):
    class Meta:
        model = ProjectExercise
        fields = ('type', 'name', 'title')
