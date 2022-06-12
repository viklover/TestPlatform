# Generated by Django 4.0.2 on 2022-06-12 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_remove_pictureimagesexercise_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseDocumentElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Заголовок'), (1, 'Изображение'), (2, 'Цитата'), (3, 'Документ'), (4, 'Карты (Yandex Maps)')], default=0, verbose_name='Тип статичного элемента')),
                ('content', models.TextField(verbose_name='Содержание документа')),
                ('name', models.CharField(max_length=100, verbose_name='Название документа')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseQuoteElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Заголовок'), (1, 'Изображение'), (2, 'Цитата'), (3, 'Документ'), (4, 'Карты (Yandex Maps)')], default=0, verbose_name='Тип статичного элемента')),
                ('quote', models.TextField(default='Цитата - очень важный элемент для теста', verbose_name='Цитата')),
                ('author', models.CharField(max_length=100, verbose_name='Автор цитаты')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseYandexMapsElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Заголовок'), (1, 'Изображение'), (2, 'Цитата'), (3, 'Документ'), (4, 'Карты (Yandex Maps)')], default=0, verbose_name='Тип статичного элемента')),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectStaticElement',
            fields=[
                ('projecttaskelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tests.projecttaskelement')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('static_element_type', models.IntegerField(choices=[(0, 'Заголовок'), (1, 'Изображение'), (2, 'Цитата'), (3, 'Документ'), (4, 'Карты (Yandex Maps)')], default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.projecttaskelement',),
        ),
        migrations.CreateModel(
            name='TitleElement',
            fields=[
                ('type', models.IntegerField(choices=[(0, 'Заголовок'), (1, 'Изображение'), (2, 'Цитата'), (3, 'Документ'), (4, 'Карты (Yandex Maps)')], default=0, verbose_name='Тип статичного элемента')),
                ('title', models.TextField(default='Новый заголовок', verbose_name='Заголовок')),
                ('static_element_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='projecttaskelement',
            name='element_type',
            field=models.IntegerField(choices=[(0, 'Упражнение'), (1, 'Статичный элемент')], default=0, verbose_name='Тип элемента'),
        ),
        migrations.CreateModel(
            name='ProjectTitleElement',
            fields=[
                ('projectstaticelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tests.projectstaticelement')),
                ('titleelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.titleelement')),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.titleelement', 'tests.projectstaticelement'),
        ),
    ]
