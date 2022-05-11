import datetime

from django.db import models
from django.contrib.auth import get_user_model


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class Test(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    icon = models.ImageField(upload_to=user_media_path, default='icon.ico')
    published = models.BooleanField(default=False)
    date_published = models.DateField(null=True)
    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')
    count_of_passes = models.IntegerField(default=0)

    def finish(self, user):
        TestFact.objects.get(test=self.id, user=user.id).finish()


class TestFact(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    started_at = models.DateField(auto_now_add=True)
    finished_at = models.DateField(null=True)

    def finish(self):
        self.finished_at = datetime.datetime.now()
