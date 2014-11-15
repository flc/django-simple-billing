from django.contrib import admin

from . import models
from .utils import get_billing_model, get_invoice_model


class BillingDataAdmin(admin.ModelAdmin):
    list_display = ('created', 'first_name', 'last_name', 'company_name', 'country')


class UserBillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing', 'label')
    raw_id_fields = ('user', 'billing')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('created', 'invoice_number')
    list_filter = ('state',)



admin.site.register(get_billing_model(), BillingDataAdmin)
admin.site.register(get_invoice_model(), InvoiceAdmin)
admin.site.register(models.UserBilling, UserBillingAdmin)
