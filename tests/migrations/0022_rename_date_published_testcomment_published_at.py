# Generated by Django 4.0.2 on 2022-05-21 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0021_rename_date_published_test_published_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcomment',
            old_name='date_published',
            new_name='published_at',
        ),
    ]