# Generated by Django 4.0.2 on 2022-05-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0033_rename_name_columnmatchexercise_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название упражнения'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='title',
            field=models.CharField(max_length=150, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='projectexercise',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название упражнения'),
        ),
        migrations.AlterField(
            model_name='projectexercise',
            name='title',
            field=models.CharField(max_length=150, null=True, verbose_name='Заголовок'),
        ),
    ]