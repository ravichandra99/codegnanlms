# Generated by Django 3.0.8 on 2020-09-02 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_certificate_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='big_title',
            field=models.CharField(default='', max_length=300),
        ),
    ]
