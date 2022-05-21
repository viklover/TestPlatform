# Generated by Django 4.0.2 on 2022-05-21 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_alter_test_date_published_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='date_published',
            new_name='published_at',
        ),
        migrations.AddField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 21, 18, 22, 58, 984272)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='project_name',
            field=models.CharField(default='NewProject', max_length=100, verbose_name='Название проекта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(default=models.CharField(max_length=100, verbose_name='Название проекта'), max_length=100, verbose_name='Название'),
        ),
    ]
