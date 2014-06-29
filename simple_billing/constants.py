from django.utils.translation import ugettext_lazy as _


INVOICE_STATE_PENDING = 10
INVOICE_STATE_PAID = 20
INVOICE_STATE_STORNO = 30
INVOICE_STATES = (
    (INVOICE_STATE_PENDING, _('Pending')),
    (INVOICE_STATE_PAID, _('Paid')),
    (INVOICE_STATE_STORNO, _('Storno')),
)
