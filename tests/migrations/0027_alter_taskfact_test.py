# Generated by Django 4.0.2 on 2022-06-17 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0026_projectexercise_max_points_taskfact_max_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskfact',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.testfact'),
        ),
    ]