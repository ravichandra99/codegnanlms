# Generated by Django 3.0.8 on 2020-09-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='trainer',
        ),
        migrations.AddField(
            model_name='course',
            name='trainer',
            field=models.ManyToManyField(to='lms.Trainer'),
        ),
    ]
