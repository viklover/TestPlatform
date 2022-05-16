
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.nickname, filename)


class User(AbstractUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to=user_media_path, default='avatar.png', verbose_name='Аватарка')

    def get_finished_tests(self):
        pass
