import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


"""
TEST MODEL
"""


class Test(models.Model):
    project_name = models.CharField(max_length=100, verbose_name='Название проекта')
    name = models.CharField(max_length=100, default=project_name, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    icon = models.ImageField(upload_to=user_media_path, default='test_icon.png')

    published = models.BooleanField(default=False)

    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')
    count_of_passes = models.IntegerField(default=0)

    def get_tasks(self):
        return Task.objects.filter(test=self).order_by('number')

    def clean(self):
        if self.id is None:
            self.name = self.project_name

    def finish(self, user):
        TestFact.objects.get(test=self.id, user=user.id).finish()

    def __render_template(self, context=None):
        if context is None:
            context = {}
        template = loader.get_template('tests/test_card.html')
        return template.render({'test': self, **context})

    def __str__(self):
        return self.__render_template()

    def get_statistics(self, user):
        return self.__render_template(
            context={
                'with_statistics': True, 'user': user
            }
        )

    def get_statistics_differences(self, user, user_page):
        return self.__render_template(
            context={
                'with_statistics': True,
                'user': user,
                'user_res': 0.16,
                'user_page': user_page,
                'user_page_res': 0.687431
            }
        )

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_name': self.project_name,
            'number_of_tasks': self.get_tasks().count(),
            'published_at': self.published_at,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }


class TestFact(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)

    def finish(self):
        self.finished_at = datetime.datetime.now()


class TestComment(models.Model):
    message = models.TextField(null=False)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    name = models.CharField(max_length=50)
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')
    number = models.IntegerField(verbose_name='Номер задания')

    title = models.TextField(default="New Task", verbose_name='Заголовок')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_json(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'test': self.test,
            'number_of_exercises': Exercise.objects.filter(task_id=self.id).count(),
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }


"""
EXERCISES MODEL
"""


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

