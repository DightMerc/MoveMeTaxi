from django.db import models


class Good(models.Model):

    description = models.TextField(
        null=False,
        blank=False,
        default=''
    )

    unit = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default=''
    )

    amount = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0
    )

    price = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0
    )

    is_vat = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    vat_rate = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0
    )

    vat_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def full_price(self):

        return self.price + self.vat_price if self.vat_price else self.price

    def __str__(self):
        return self.description


class Company(models.Model):

    tin = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        default=0,
    )

    title = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        default=''
    )

    address = models.TextField(
        null=False,
        blank=False
    )

    main_phone = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )

    mobile_phone = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )

    checking_account = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    mfo = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    region = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    district = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    oked = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    head_manager = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    head_account_manager = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    released_by = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    is_vat = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    excise_tax = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    sms_inform = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.title}: {self.tin}'


class Status(models.Model):

    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Invoice(models.Model):

    invoice_number = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        default=0
    )

    invoice_date = models.DateTimeField(
        null=False,
        blank=False,
    )

    contract_number = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    contract_date = models.DateTimeField(
        null=False,
        blank=False,
    )

    is_authorited = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    authority_number = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        default=0
    )

    authority_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    authorited_person = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    is_one_side_invoice = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    created_by = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    invoiced_from = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='invoiced_from'
    )

    invoiced_to = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='invoiced_to'
    )

    goods = models.ManyToManyField(
        Good,
        blank=False
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    file = models.FileField(
        null=True,
        blank=True,
        upload_to='uploads/docs/%Y/%m/%d/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
