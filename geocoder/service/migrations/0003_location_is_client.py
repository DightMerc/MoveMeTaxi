# Generated by Django 3.1.5 on 2021-01-19 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210112_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='is_client',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
