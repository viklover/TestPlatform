# Generated by Django 4.0.3 on 2022-06-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronologyexercise',
            name='exercise_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='matchexercise',
            name='exercise_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
