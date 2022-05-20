import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class Test(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    icon = models.ImageField(upload_to=user_media_path, default='icon.ico')
    published = models.BooleanField(default=False)
    date_published = models.DateTimeField(null=True)
    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')
    count_of_passes = models.IntegerField(default=0)

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
    date_published = models.DateTimeField(default=timezone.now)
