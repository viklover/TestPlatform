# Generated by Django 4.0.2 on 2022-05-10 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_test_count_of_passes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='icon_url',
        ),
        migrations.AddField(
            model_name='test',
            name='icon',
            field=models.ImageField(blank=True, default='icon.ico', upload_to='avatars'),
        ),
    ]
