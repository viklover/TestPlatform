from importlib._common import _

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class Task(models.Model):
    number = models.IntegerField()
    result = models.FloatField()
    finished = models.BooleanField(default=None)


class Session(models.Model):
    nickname = models.CharField(max_length=45)
    points = models.FloatField(default=None)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    finished = models.DateTimeField(default=None)
    started = models.DateTimeField(default=timezone.now())


class User(AbstractUser):
    current_session = models.ForeignKey(Session, on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')

