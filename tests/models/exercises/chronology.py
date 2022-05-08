
from django.db import models

from tests.models.exercises.exercise import Exercise


class ChronologyExercise(Exercise):
    type = 5


class VariantChronologyExercise(Exercise):
    exercise = models.ForeignKey(to=ChronologyExercise, on_delete=models.CASCADE)
    name = models.TextField()
    order = models.IntegerField(verbose_name='Порядковый номер')
