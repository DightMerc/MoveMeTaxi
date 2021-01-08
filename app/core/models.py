from django.db import models

from datetime import datetime

import hashlib


class DeviceType(models.Model):

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    code = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.code} - {self.title}'


class Device(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    notificationID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        default=None,
        null=False
    )

    verified = models.BooleanField(
        default=False,
        null=True,
        blank=False
    )

    verification_code = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.GUID} - {self.type.title}'


class Language(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class RideStatus(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(RideStatus, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserStatus(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(UserStatus, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProfilePhoto(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to='photo/profile/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(ProfilePhoto, self).save(*args, **kwargs)

    def __str__(self):
        return self.GUID


class CarPhoto(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to='photo/car/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(CarPhoto, self).save(*args, **kwargs)

    def __str__(self):
        return self.GUID


class CoreUser(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    email = models.EmailField(
        null=True,
        blank=True,
        default=None
    )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    phone = models.BigIntegerField(
        null=False,
        blank=False,
        default=0
    )

    firstname = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    surname = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    photo = models.ForeignKey(
        ProfilePhoto,
        on_delete=models.CASCADE,
        default=None,
        blank=True
    )

    status = models.ForeignKey(
        UserStatus,
        on_delete=models.CASCADE,
        default=None,
        blank=True
    )

    devices = models.ManyToManyField(
        Device
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(CoreUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.firstname + "asd"


class Partner(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    drivers = models.ManyToManyField(
        'Driver',
        related_name='partner_drivers'
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Partner, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CarModel(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(CarModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CarColor(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    hash = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(CarColor, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Car(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    manufacturer = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    color = models.ForeignKey(
        CarColor,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    photo = models.ForeignKey(
        CarPhoto,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    year = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    number = models.CharField(
        max_length=255,
        default='',
        null=False,
        blank=False
    )

    conditioner = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    registration_date = models.DateTimeField(
        default=datetime.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Car, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.model} - {self.number}'


class FarePolicy(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    price_per_kilometer = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    price_per_minute_of_waiting = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    price_for_rating = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    price_for_conditioner = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    price_for_out_of_town = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    price_for_car_model = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    temp = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    started_at = models.DateTimeField(
        default=datetime.now,
        null=False,
        blank=False
    )

    closes_at = models.DateTimeField(
        default=datetime.now,
        null=False,
        blank=False
    )

    active = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(FarePolicy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Driver(models.Model):

    user = models.ForeignKey(
        CoreUser,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    rating = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    fare_policy = models.ForeignKey(
        FarePolicy,
        on_delete=models.CASCADE,
        default=None,
        blank=True
    )

    def __str__(self):
        return self.user.firstname


class Client(models.Model):

    user = models.ForeignKey(
        CoreUser,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    rating = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.firstname


class Address(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    latitude = models.CharField(
        max_length=20,
        default='',
        null=False,
        blank=False
    )

    longitude = models.CharField(
        max_length=20,
        default='',
        null=False,
        blank=False
    )

    house = models.CharField(
        max_length=20,
        default='',
        null=False,
        blank=False
    )

    comment = models.CharField(
        max_length=256,
        default='',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PaymentType(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100,
        default='',
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(PaymentType, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    stars = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    comment = models.CharField(
        max_length=1024,
        default='',
        null=True,
        blank=True
    )

    reason = models.CharField(
        max_length=1024,
        default='',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Review, self).save(*args, **kwargs)


class Ride(models.Model):

    GUID = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    price = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    start_point = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        default=None,
        blank=False,
        related_name='start_address'
    )

    end_point = models.ManyToManyField(
        Address,
        blank=True,
    )

    payment_type = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    status = models.ForeignKey(
        RideStatus,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    def save(self, *args, **kwargs):
        if not self.GUID:
            self.GUID = hashlib.md5(
                str(datetime.now()).encode('utf-8')
                ).hexdigest()
        super(Review, self).save(*args, **kwargs)
