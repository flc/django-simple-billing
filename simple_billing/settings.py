from django.conf import settings


BILLING_DATA_MODEL = getattr(settings, 'SIMPLE_BILLING_DATA_MODEL', 'simple_billing.BillingData')
INVOICE_MODEL = getattr(settings, 'SIMPLE_BILLING_INVOICE_MODEL', 'simple_billing.Invoice')
INVOICE_FROM = settings.SIMPLE_BILLING_INVOICE_FROM  # required setting
INVOICE_IMG_PATH = getattr(settings, 'SIMPLE_BILLING_INVOICE_IMG_PATH', '')
DECIMAL_PLACES = getattr(settings, 'SIMPLE_BILLING_DECIMAL_PLACES', 2)
MAX_DIGITS = getattr(settings, 'SIMPLE_BILLING_MAX_DIGITS', 10)
DEFAULT_INVOICE_PREFIX = getattr(settings, 'SIMPLE_BILLING_DEFAULT_INVOICE_PREFIX', '')
INVOICE_FILES_DIR = settings.SIMPLE_BILLING_INVOICE_FILES_DIR  # required setting
