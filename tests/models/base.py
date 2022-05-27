import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class BaseTask(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(verbose_name='Номер задания')
    title = models.TextField(default="New Task", verbose_name='Заголовок')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseExercise(models.Model):
    EXERCISE_TYPES = (
        (0, 'answer'),
        (1, 'input'),
        (2, 'statements'),
        (3, 'radio'),
        (4, 'match'),
        (5, 'chronology')
    )
    type = models.IntegerField(choices=EXERCISE_TYPES, verbose_name='Тип упражнения')
    title = models.TextField(null=True)

    class Meta:
        abstract = True

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        template = loader.get_template(template)
        return template.render({'exercise': self, **context})


class BaseTestInfo(models.Model):
    name = models.CharField(max_length=100, default='New test', verbose_name='Название')
    description = models.TextField(default='Description', verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    icon = models.ImageField(upload_to=user_media_path, default='test_icon.png')

    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')

    class Meta:
        abstract = True
