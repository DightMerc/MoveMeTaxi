# Generated by Django 3.1.5 on 2021-01-08 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210108_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='fare_policy',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.farepolicy'),
        ),
    ]
