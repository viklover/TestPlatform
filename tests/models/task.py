
from django.db import models

from tests.models.test import Test


class Task(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')
    number = models.IntegerField(verbose_name='Номер задания')

