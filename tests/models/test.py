import datetime

from django.db import models
from django.contrib.auth import get_user_model


class Test(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    icon_url = models.TextField(null=True, verbose_name='Путь к иконке')

    def finish(self, user):
        TestFact.objects.get(test=self.id, user=user.id).finish()


class TestFact(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    started_at = models.DateField(auto_now_add=True)
    finished_at = models.DateField(null=True)

    def finish(self):
        self.finished_at = datetime.datetime.now()


