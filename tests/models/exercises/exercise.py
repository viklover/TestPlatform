
from django.db import models

from tests.models.task import Task


class Exercise(models.Model):
    TYPES = (
        (0, 'answer'),
        (1, 'input'),
        (2, 'statements'),
        (3, 'radio'),
        (4, 'match'),
        (5, 'chronology')
    )
    task = models.ForeignKey(to=Task, on_delete=models.SET_NULL, null=True, verbose_name='Задание')
    type = models.IntegerField(choices=TYPES, verbose_name='Тип упражнения')
