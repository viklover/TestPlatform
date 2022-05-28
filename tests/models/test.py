import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone

from tests.models.base import BaseTestInfo, BaseTask, BaseExercise, BaseModel


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


"""
PROJECT MODEL
"""


class Project(BaseModel, BaseTestInfo):
    project_name = models.CharField(max_length=100, verbose_name='Название проекта')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    published = models.BooleanField(default=False)

    def get_tasks(self):
        return ProjectTask.objects.filter(project=self).order_by('number')

    @staticmethod
    def edit_info(form):

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return project

        return False

    def create_task(self, form):

        if form.is_valid():
            task = form.save(commit=False)
            task.number = self.get_tasks().count() + 1
            task.save()
            return task

        return None

    def create(self, form):

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return self

        return False


class ProjectTask(BaseModel, BaseTask):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def edit_info(form):

        if form.is_valid():
            task = form.save(commit=False)
            task.save()


class ProjectExercise(BaseModel, BaseExercise):
    task = models.ForeignKey(to=ProjectTask, on_delete=models.CASCADE, null=True)


"""
TEST MODEL
"""


class Test(BaseModel, BaseTestInfo):
    current_version = models.IntegerField(default=1)

    def get_test(self):
        return TestVersion.objects.get(test=self, version=self.current_version)

    def get_versions(self):
        return TestVersion.objects.filter(test=self)


class TestVersion(BaseModel):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    version = models.IntegerField()
    published_at = models.DateTimeField(null=True)

    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')


class TestFact(BaseModel):
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Испытуемый',
                             related_name='person')

    def finish(self):
        self.finished_at = datetime.datetime.now()
        self.completed = True
        self.save()


class TestComment(BaseModel):
    message = models.TextField(null=False)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)


class Task(BaseModel, BaseTask):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')


"""
EXERCISES MODEL
"""


class Exercise(BaseModel, BaseExercise):
    pass


"""
CHRONOLOGY EXERCISE MODEL
"""


class ChronologyExercise(Exercise):
    type = 5


class VariantChronologyExercise(Exercise):
    exercise = models.ForeignKey(to=ChronologyExercise, on_delete=models.CASCADE)
    content = models.TextField()
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
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class VariantMatchExercise(models.Model):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    column = models.ForeignKey(to=ColumnMatchExercise, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content

