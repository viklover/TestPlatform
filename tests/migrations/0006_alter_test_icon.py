# Generated by Django 4.0.2 on 2022-05-10 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_remove_test_icon_url_test_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='icon',
            field=models.ImageField(blank=True, default='icon.ico', upload_to='tests/uploaded_icons'),
        ),
    ]
