# Generated by Django 4.0.2 on 2022-06-11 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_project_description_md_test_description_md'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='description_md',
            field=models.TextField(default='Объяснение задания\n======='),
        ),
        migrations.AddField(
            model_name='task',
            name='description_md',
            field=models.TextField(default='Объяснение задания\n======='),
        ),
        migrations.AlterField(
            model_name='project',
            name='description_md',
            field=models.TextField(default='Test info\n======='),
        ),
        migrations.AlterField(
            model_name='test',
            name='description_md',
            field=models.TextField(default='Test info\n======='),
        ),
    ]
