from rest_framework import serializers

from core import models
from django.conf import settings


class DeviceTypeSerializer(serializers.Serializer):

    title = serializers.CharField()
    code = serializers.IntegerField


class DeviceSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    notificationID = serializers.CharField()


class UserStatusSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()


class UserPhotoSerializer(serializers.Serializer):

    def to_representation(self, value):
        return f'{settings.MEDIA_SITE_URL}{settings.MEDIA_URL}{value.photo}'
        # return f'{value.photo}'


class LanguageSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()


class CoreUserSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    language = LanguageSerializer()
    email = serializers.CharField()
    phone = serializers.CharField()
    status = UserStatusSerializer()
    firstname = serializers.CharField()
    surname = serializers.CharField()
    photo = UserPhotoSerializer()


class CarModelSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()


class CarColorSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()
    hash = serializers.CharField()


class CarPhotoSerizlizer(serializers.Serializer):

    def to_representation(self, value):
        return f'{settings.MEDIA_SITE_URL}{settings.MEDIA_URL}{value.photo}'


class CarSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    manufacturer = serializers.CharField()
    model = CarModelSerializer()
    color = CarColorSerializer()
    photo = CarPhotoSerizlizer()
    year = serializers.IntegerField()
    number = serializers.CharField()
    conditioner = serializers.BooleanField()
    registration_date = serializers.DateTimeField()


class ClientSerializer(serializers.Serializer):

    user = CoreUserSerializer()
    rating = serializers.IntegerField()


class DriverSerializer(serializers.Serializer):

    user = CoreUserSerializer()
    rating = serializers.IntegerField()
    car = CarSerializer()


class AddressSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    entrance = serializers.CharField()
    comment = serializers.CharField()


class PaymentTypeSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()


class ReviewSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    stars = serializers.IntegerField()
    comment = serializers.CharField()
    reason = serializers.CharField()


class RideStatusSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()


class RideSerializer(serializers.Serializer):

    GUID = serializers.CharField()
    client = ClientSerializer()
    driver = DriverSerializer()
    price = serializers.IntegerField()
    start_point = AddressSerializer()
    end_point = AddressSerializer(many=True)
    payment_type = PaymentTypeSerializer()
    review = ReviewSerializer()
    status = RideStatusSerializer()


class FarePolicySerizlier(serializers.Serializer):

    GUID = serializers.CharField()
    title = serializers.CharField()
    price_per_kilometer = serializers.FloatField()
    price_per_minute_of_waiting = serializers.FloatField()
    # price_for_rating = serializers.FloatField()
    price_for_conditioner = serializers.FloatField()
    # price_for_out_of_town = serializers.FloatField()
    # price_for_car_model = serializers.FloatField()
