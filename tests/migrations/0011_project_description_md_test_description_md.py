# Generated by Django 4.0.2 on 2022-06-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_projecttaskelement_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description_md',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='description_md',
            field=models.TextField(null=True),
        ),
    ]
