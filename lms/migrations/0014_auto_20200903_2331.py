# Generated by Django 3.0.8 on 2020-09-03 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0013_auto_20200903_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videoreviews',
            old_name='video_link',
            new_name='embed_link',
        ),
        migrations.RenameField(
            model_name='videoreviews',
            old_name='video_name',
            new_name='title',
        ),
    ]
