from rest_framework import serializers

from core import models


class CompanySerializer(serializers.Serializer):

    tin = serializers.IntegerField()
    title = serializers.CharField()
    address = serializers.CharField()
    main_phone = serializers.IntegerField()
    mobile_phone = serializers.IntegerField()
    checking_account = serializers.CharField()
    mfo = serializers.CharField()
    region = serializers.CharField()
    district = serializers.CharField()
    oked = serializers.CharField()
    head_manager = serializers.CharField()
    head_account_manager = serializers.CharField()
    released_by = serializers.CharField()
    is_vat = serializers.BooleanField()
    excise_tax = serializers.BooleanField()
    sms_inform = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GoodSerializer(serializers.Serializer):

    description = serializers.CharField()
    unit = serializers.CharField()
    amount = serializers.IntegerField()
    price = serializers.IntegerField()
    is_vat = serializers.BooleanField()
    vat_rate = serializers.IntegerField()
    vat_price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class StatusSerializer(serializers.Serializer):

    title = serializers.CharField()


class InvoiceSerializer(serializers.Serializer):

    invoice_number = serializers.IntegerField()
    invoice_date = serializers.DateTimeField()
    contract_number = serializers.CharField()
    contract_date = serializers.DateTimeField()
    is_authorited = serializers.BooleanField()
    authority_number = serializers.IntegerField()
    authority_date = serializers.DateTimeField()
    authorited_person = serializers.CharField()
    is_one_side_invoice = serializers.BooleanField()
    created_by = serializers.CharField()
    invoiced_from = CompanySerializer()
    invoiced_to = CompanySerializer()
    goods = GoodSerializer(many=True)
    status = StatusSerializer()
    file = serializers.FileField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
