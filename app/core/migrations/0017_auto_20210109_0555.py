# Generated by Django 3.1.5 on 2021-01-09 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210109_0539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='login',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='password',
        ),
    ]
