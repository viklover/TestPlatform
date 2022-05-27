import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone

from tests.models.base import BaseTestInfo, BaseTask, BaseExercise


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


"""
PROJECT MODEL
"""


class Project(BaseTestInfo):
    project_name = models.CharField(max_length=100, verbose_name='Название проекта')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_tasks(self):
        return ProjectTask.objects.filter(project=self).order_by('number')


class ProjectTask(BaseTask):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectExercise(BaseExercise):
    task = models.ForeignKey(to=ProjectTask, on_delete=models.CASCADE, null=True)


"""
TEST MODEL
"""


class Test(models.Model):
    current_version = models.IntegerField(default=1)


class TestVersion(BaseTestInfo):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    version = models.IntegerField()
    published_at = models.DateTimeField(null=True)


class TestFact(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Испытуемый',
                             related_name='person')


class TestComment(models.Model):
    message = models.TextField(null=False)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)


class Task(BaseTask):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')


"""
EXERCISES MODEL
"""


class Exercise(BaseExercise):
    pass


"""
CHRONOLOGY EXERCISE MODEL
"""


class ChronologyExercise(Exercise):
    type = 5


class VariantChronologyExercise(Exercise):
    exercise = models.ForeignKey(to=ChronologyExercise, on_delete=models.CASCADE)
    name = models.TextField()
    order = models.IntegerField(verbose_name='Порядковый номер')


"""
MATCH EXERCISE MODEL
"""


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

