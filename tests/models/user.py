
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class User(AbstractUser):
    nickname = models.CharField(max_length=25)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=user_media_path, default='avatar.png')

    def get_finished_tests(self):
        pass
