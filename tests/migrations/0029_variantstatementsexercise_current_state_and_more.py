# Generated by Django 4.0.2 on 2022-06-18 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0028_variantmatchexercise_current_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantstatementsexercise',
            name='current_state',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='projectexercise',
            name='exercise_type',
            field=models.IntegerField(choices=[(0, 'Ответить на вопрос'), (1, 'Написать развёрнутый ответ'), (2, 'Отметить верные утверждения'), (3, 'Выбрать одно верное утверждение'), (4, 'Соотнести что-то с чем-то'), (5, 'Составить правильный порядок карточек'), (6, 'Выбери подходящие изображения'), (7, 'Соотнеси что-то с элементом из списка')], default=0),
        ),
        migrations.AlterField(
            model_name='testfactexercise',
            name='exercise_type',
            field=models.IntegerField(choices=[(0, 'Ответить на вопрос'), (1, 'Написать развёрнутый ответ'), (2, 'Отметить верные утверждения'), (3, 'Выбрать одно верное утверждение'), (4, 'Соотнести что-то с чем-то'), (5, 'Составить правильный порядок карточек'), (6, 'Выбери подходящие изображения'), (7, 'Соотнеси что-то с элементом из списка')], default=0),
        ),
    ]