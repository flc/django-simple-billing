from django.db.models.loading import get_model

from . import settings as app_settings


def get_billing_model():
    return get_model(*app_settings.BILLING_DATA_MODEL.rsplit('.', 1))


def get_invoice_model():
    return get_model(*app_settings.INVOICE_MODEL.rsplit('.', 1))


def get_invoice_item_model():
    return get_model(*app_settings.INVOICE_ITEM_MODEL.rsplit('.', 1))
