# Generated by Django 3.0.8 on 2020-09-03 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0010_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimonials',
            old_name='image396x390',
            new_name='image',
        ),
    ]
