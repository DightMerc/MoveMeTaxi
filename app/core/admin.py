from django.contrib import admin
from core import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'tin',
                    'title',
                    'address',
                    'main_phone',
                    'mobile_phone',
                    'checking_account',
                    'mfo',
                    'region',
                    'district',
                    'oked',
                    'head_manager',
                    'head_account_manager',
                    'released_by',
                    'is_vat',
                    'excise_tax',
                    'sms_inform',
                    'created_at',
                    'updated_at')

    ordering = ('id',
                'tin',
                'region',
                'oked',
                'is_vat',
                'created_at',
                'updated_at')

    search_fields = (
        'id',
        'tin',
        'region',
        'district',
        )


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'unit',
                    'amount',
                    'price',
                    'is_vat',
                    'vat_rate',
                    'vat_price',
                    'created_at',
                    'updated_at',
                    'FullPrice',
                    )

    def FullPrice(self, obj):
        return obj.full_price()
    FullPrice.admin_order_field = 'full_price'
    FullPrice.short_description = 'Full Price'

    ordering = ('id',
                'price',
                'vat_price'
                )

    search_fields = (
        'id',
        )


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'invoice_number',
                    'invoice_date',
                    'contract_number',
                    'contract_date',
                    'is_authorited',
                    'authority_number',
                    'authority_date',
                    'authorited_person',
                    'is_one_side_invoice',
                    'created_by',
                    'invoiced_from',
                    'invoiced_to',
                    'status',
                    'created_at',
                    'updated_at',
                    )

    ordering = ('id',
                'invoice_number',
                'invoice_date',
                'is_authorited',
                'invoiced_from',
                'invoiced_to',
                'created_at',
                'updated_at')

    search_fields = (
        'id',
        )


admin.site.register(models.Status)
