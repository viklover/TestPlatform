# Generated by Django 4.0.2 on 2022-06-12 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0018_documentelement_pictureelement_quoteelement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictureelement',
            name='picture',
            field=models.ImageField(default='picture.jpg', upload_to='project/static_pictures', verbose_name='Изображение'),
        ),
    ]
