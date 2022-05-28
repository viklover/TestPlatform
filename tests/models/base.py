import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class BaseModel(models.Model):

    def get_json(self):
        data = {}
        for field in self._meta.local_fields:
            data[field.name] = getattr(self, field.name)
        return data

    def copy_fields_from(self, model, except_fields=None):
        if except_fields is None:
            except_fields = []
        for field in model._meta.local_fields:
            if field.name not in except_fields:
                self._meta.local_fields[field.name] = getattr(model, field.name)

    class Meta:
        abstract = True


class BaseTask(BaseModel):
    name = models.CharField(max_length=50)
    number = models.IntegerField(verbose_name='Номер задания')
    title = models.TextField(default="New Task", verbose_name='Заголовок')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseExercise(BaseModel):
    EXERCISE_TYPES = (
        (0, 'Ответить на вопрос'),
        (1, 'Написать развёрнутый ответ'),
        (2, 'Отметить верные утверждения'),
        (3, 'Выбрать одно верное утверждение'),
        (4, 'Соотнести что-то с чем-то'),
        (5, 'Составить правильный порядок карточек')
    )
    EXERCISE_CLASSES = {
        0: 'AnswerExercise',
        1: 'InputExercise',
        2: 'StatementsExercise',
        3: 'RadioExercise',
        4: 'MatchExercise',
        5: 'ChronologyExercise'
    }
    type = models.IntegerField(choices=EXERCISE_TYPES, default=0, verbose_name='Тип упражнения')
    name = models.CharField(max_length=50, verbose_name='Название упражнения')
    title = models.CharField(max_length=150, null=True, verbose_name='Заголовок')

    class Meta:
        abstract = True

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        template = loader.get_template(template)
        return template.render({'exercise': self, **context})


class BaseTestInfo(BaseModel):
    name = models.CharField(max_length=100, default='New test', verbose_name='Название')
    description = models.TextField(default='Description', verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    icon = models.ImageField(upload_to=user_media_path, default='test_icon.png')

    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')

    class Meta:
        abstract = True


class BaseProject(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update(self):
        self.updated_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
