# Generated by Django 3.1.5 on 2021-01-19 11:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('latitude', models.CharField(default='', max_length=20)),
                ('longitude', models.CharField(default='', max_length=20)),
                ('house', models.CharField(default='', max_length=20)),
                ('comment', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('manufacturer', models.CharField(default='', max_length=100)),
                ('year', models.IntegerField(default=0)),
                ('number', models.CharField(default='', max_length=255)),
                ('conditioner', models.BooleanField(default=False)),
                ('registration_date', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('hash', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('photo', models.ImageField(upload_to='photo/car/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoreUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('phone', models.BigIntegerField(default=0)),
                ('firstname', models.CharField(default='', max_length=100)),
                ('surname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('code', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('car', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.car')),
            ],
        ),
        migrations.CreateModel(
            name='FarePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('price_per_kilometer', models.FloatField(default=0)),
                ('price_per_minute_of_waiting', models.FloatField(default=0)),
                ('price_for_rating', models.FloatField(default=0)),
                ('price_for_conditioner', models.FloatField(default=0)),
                ('price_for_out_of_town', models.FloatField(default=0)),
                ('price_for_car_model', models.FloatField(default=0)),
                ('temp', models.BooleanField(default=False)),
                ('started_at', models.DateTimeField(default=datetime.datetime.now)),
                ('closes_at', models.DateTimeField(default=datetime.datetime.now)),
                ('active', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('photo', models.ImageField(upload_to='photo/profile/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('stars', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('reason', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RideStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('price', models.FloatField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.client')),
                ('driver', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.driver')),
                ('end_point', models.ManyToManyField(blank=True, to='core.Address')),
                ('fare_policy', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.farepolicy')),
                ('payment_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.paymenttype')),
                ('review', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.review')),
                ('start_point', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='start_address', to='core.address')),
                ('status', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.ridestatus')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('drivers', models.ManyToManyField(related_name='partner_drivers', to='core.Driver')),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='fare_policy',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.farepolicy'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser'),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GUID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('notificationID', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('verified', models.BooleanField(default=False, null=True)),
                ('active', models.BooleanField(default=True)),
                ('verification_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.devicetype')),
            ],
        ),
        migrations.AddField(
            model_name='coreuser',
            name='devices',
            field=models.ManyToManyField(blank=True, to='core.Device'),
        ),
        migrations.AddField(
            model_name='coreuser',
            name='language',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.language'),
        ),
        migrations.AddField(
            model_name='coreuser',
            name='photo',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.profilephoto'),
        ),
        migrations.AddField(
            model_name='coreuser',
            name='status',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.userstatus'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.carcolor'),
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.carphoto'),
        ),
    ]
