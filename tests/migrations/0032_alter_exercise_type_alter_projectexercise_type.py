# Generated by Django 4.0.2 on 2022-05-28 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0031_project_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='type',
            field=models.IntegerField(choices=[(0, 'Ответить на вопрос'), (1, 'Написать развёрнутый ответ'), (2, 'Отметить верные утверждения'), (3, 'Выбрать одно верное утверждение'), (4, 'Соотнести что-то с чем-то'), (5, 'Составить правильный порядок карточек')], verbose_name='Тип упражнения'),
        ),
        migrations.AlterField(
            model_name='projectexercise',
            name='type',
            field=models.IntegerField(choices=[(0, 'Ответить на вопрос'), (1, 'Написать развёрнутый ответ'), (2, 'Отметить верные утверждения'), (3, 'Выбрать одно верное утверждение'), (4, 'Соотнести что-то с чем-то'), (5, 'Составить правильный порядок карточек')], verbose_name='Тип упражнения'),
        ),
    ]
