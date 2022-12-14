# Generated by Django 4.0.2 on 2022-06-14 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_remove_yandexmapselement_url_yandexmapselement_frame'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyMatchListExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MatchListExercise',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='Название упражнения')),
                ('title', models.CharField(max_length=150, null=True, verbose_name='Заголовок')),
                ('exercise_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='projectexercise',
            name='exercise_type',
            field=models.IntegerField(choices=[(0, 'Ответить на вопрос'), (1, 'Написать развёрнутый ответ'), (2, 'Отметить верные утверждения'), (3, 'Выбрать одно верное утверждение'), (4, 'Соотнести что-то с чем-то'), (7, 'Соотнеси что-то с элементом из списка'), (5, 'Составить правильный порядок карточек'), (6, 'Выбери подходящие изображения')], default=0),
        ),
        migrations.CreateModel(
            name='ProjectMatchListExercise',
            fields=[
                ('projectexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tests.projectexercise')),
                ('matchlistexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.matchlistexercise')),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.matchlistexercise', 'tests.projectexercise'),
        ),
        migrations.CreateModel(
            name='ValueMatchListExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.matchlistexercise')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.keymatchlistexercise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='keymatchlistexercise',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.matchlistexercise'),
        ),
    ]
