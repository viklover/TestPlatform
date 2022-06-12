from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import Project, ProjectTask, BaseExercise, BaseElement, \
    ProjectChronologyExercise, ProjectMatchExercise, ProjectRadioExercise, \
    ProjectStatementsExercise, ProjectInputExercise, ProjectAnswerExercise, ProjectImagesExercise, \
    ProjectImagesExercise, PictureImagesExercise, ProjectTitleElement, ProjectPictureElement, \
    ProjectQuoteElement, ProjectDocumentElement, ProjectYandexMapsElement
from tests.models.base import BaseStaticElement


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


class ExcludedModelForm(ModelForm):
    class Meta:
        fields = ['type', 'name', 'title']


class CreationExerciseForm(forms.Form):
    type = forms.ChoiceField(choices=BaseExercise.EXERCISE_TYPES, required=True, label='Тип упражнения')
    name = forms.CharField(max_length=50, required=True, label='Название')
    title = forms.CharField(max_length=150, required=False, label='Заголовок (необязательно)')

    def get_exercise(self):
        exercise = eval(f'Project{BaseExercise.EXERCISE_CLASSES[int(self.cleaned_data["type"])]}()')
        exercise.type = self.cleaned_data['type']
        exercise.name = self.cleaned_data['name']
        exercise.title = self.cleaned_data['title']
        return exercise


class CreationStaticElementForm(forms.Form):
    type = forms.ChoiceField(choices=BaseStaticElement.ELEMENT_TYPES, required=True, label='Тип статичного элемента')

    def get_element(self):
        element = eval(f'Project{BaseStaticElement.ELEMENT_CLASSES[int(self.cleaned_data["type"])]}()')
        element.type = self.cleaned_data['type']
        return element


class CheckMarkDownForm(forms.Form):
    markdown_field = forms.Textarea()
