# Generated by Django 4.0.2 on 2022-06-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0014_alter_projectexercise_exercise_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pictureimagesexercise',
            name='url',
        ),
        migrations.AddField(
            model_name='pictureimagesexercise',
            name='image',
            field=models.ImageField(default=None, upload_to='project/images_exercise'),
            preserve_default=False,
        ),
    ]
