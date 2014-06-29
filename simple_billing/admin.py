from django.contrib import admin

from . import models
from .utils import get_billing_model, get_invoice_model


class BillingDataAdmin(admin.ModelAdmin):
    list_display = ('created',)
    search_fields = ('=id',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('created', 'invoice_number')
    list_filter = ('state',)


admin.site.register(get_billing_model(), BillingDataAdmin)
admin.site.register(get_invoice_model(), InvoiceAdmin)
admin.site.register(models.UserBilling)
