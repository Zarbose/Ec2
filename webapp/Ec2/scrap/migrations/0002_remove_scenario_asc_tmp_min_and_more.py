# Generated by Django 4.1.7 on 2023-05-15 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='asc_tmp_min',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='asc_tmp_min_choices',
        ),
    ]
