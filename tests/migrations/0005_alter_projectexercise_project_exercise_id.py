# Generated by Django 4.0.3 on 2022-06-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_projectexercise_project_exercise_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectexercise',
            name='project_exercise_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
