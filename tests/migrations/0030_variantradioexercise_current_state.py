# Generated by Django 4.0.2 on 2022-06-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0029_variantstatementsexercise_current_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantradioexercise',
            name='current_state',
            field=models.BooleanField(default=False),
        ),
    ]
