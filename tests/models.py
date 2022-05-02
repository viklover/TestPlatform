from django.db import models
from django.contrib.auth import get_user_model

class MatchExercise(Exercise):
    type = 2

    @staticmethod
    def get_columns(self):
        return ColumnMatchExercise.objects.filter(exercise_id=self.id)

    @staticmethod
    def get_variants(self):
        return VariantMatchExercise.objects.filter(exercise_id=self.id)

class ColumnMatchExercise(models.Model):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VariantMatchExercise(models.Model):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    column = models.ForeignKey(to=ColumnMatchExercise, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
