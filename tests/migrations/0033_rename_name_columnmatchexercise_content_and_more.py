# Generated by Django 4.0.2 on 2022-05-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0032_alter_exercise_type_alter_projectexercise_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='columnmatchexercise',
            old_name='name',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='variantchronologyexercise',
            old_name='name',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='variantmatchexercise',
            old_name='name',
            new_name='content',
        ),
        migrations.AddField(
            model_name='exercise',
            name='name',
            field=models.CharField(default='New exercise', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectexercise',
            name='name',
            field=models.CharField(default='New exercise', max_length=50),
            preserve_default=False,
        ),
    ]