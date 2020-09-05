# Generated by Django 3.0.8 on 2020-09-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_auto_20200902_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='img1240x600',
        ),
        migrations.RemoveField(
            model_name='course',
            name='reviews',
        ),
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.FloatField(default=4.8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='img293x274',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('question', models.ManyToManyField(to='lms.CertQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='certification',
            field=models.ManyToManyField(to='lms.Certificate'),
        ),
    ]