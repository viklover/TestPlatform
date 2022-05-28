# Generated by Django 4.0.2 on 2022-05-27 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0027_project_remove_exercise_task_remove_test_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]