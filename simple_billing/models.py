import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import F

from django_countries.fields import CountryField
from djmoney.models.fields import CurrencyField, MoneyField
from moneyed import Money

from . import settings as app_settings
from .pdf_utils import generate_pdf
from .constants import *


logger = logging.getLogger(__name__)


class BillingDataBase(models.Model):
    first_name = models.TextField(
        _(u"First Name"),
        blank=True,
        )
    last_name = models.TextField(
        _(u"Last name"),
        blank=True,
        )
    company_name = models.TextField(
        _(u"Institution / Company name"),
        blank=True,
        )
    email = models.EmailField(
        _(u"Email"),
        blank=True,
        max_length=200,
        )
    phone = models.CharField(
        _(u"Phone"),
        max_length=30,
        blank=True,
        )
    country = CountryField(
        _(u"Country"),
        blank=True,
        )
    state = models.TextField(
        _(u"State / Province"),
        blank=True,
        )
    post_code = models.CharField(
        _(u"ZIP / Post code"),
        max_length=20,
        blank=True,
        )
    city = models.TextField(
        _(u"City"),
        blank=True,
        )
    address_1 = models.TextField(
        _(u"Address"),
        blank=True,
        )
    address_2 = models.TextField(
        _("Address 2"),
        blank=True,
        )
    tax_id = models.CharField(
        _("Tax ID"),
        max_length=50,
        blank=True,
        )
    created = models.DateTimeField(
        _(u"created"),
        auto_now_add=True,
        )
    updated = models.DateTimeField(
        _(u"updated"),
        auto_now=True,
        )

    class Meta:
        abstract = True


class BillingData(BillingDataBase):
    pass


class UserBilling(models.Model):
    # allow users to have more than one billing data
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="billing",
        )
    billing = models.OneToOneField(
        app_settings.BILLING_DATA_MODEL,
        )
    label = models.TextField(
        _(u"Label"),
        blank=True,
        default="default",
        )


class InvoiceBase(models.Model):
    billing = models.ForeignKey(
        "UserBilling",
        related_name="invoices",
        )
    invoice_number = models.TextField(
        _(u"Invoice No."),
        )
    issue_date = models.DateField(
        _(u"Issue date"),
        )
    due_date = models.DateField(
        _(u"Due date"),
        null=True, blank=True,
        )
    fulfilment_date = models.DateField(
        _(u"Fulfilment date"),
        null=True, blank=True,
        )
    payment_method = models.TextField(
        _(u"method of payment"),
        blank=True,
        )
    currency = CurrencyField(
        _(u"currency"),
        )
    state = models.PositiveSmallIntegerField(
        _(u"state"),
        default=INVOICE_STATE_PENDING,
        choices=INVOICE_STATES,
        )
    created = models.DateTimeField(
        _(u"created"),
        auto_now_add=True,
        )
    file = models.FileField(
        _(u"file"),
        blank=True,
        upload_to='invoices',
        storage= FileSystemStorage(location=app_settings.INVOICE_FILES_DIR),
        )

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.invoice_number

    @property
    def total(self):
        return sum(item.total for item in self.items.iterator())

    def get_render_context(self):
        return {
            'invoice': self,
            'invoice_items': self.items.all(),
            'billing': self.billing.billing,
            'invoice_from': app_settings.INVOICE_FROM,
            'invoice_from_lines': app_settings.INVOICE_FROM.splitlines(),
            'invoice_img_path': app_settings.INVOICE_IMG_PATH,
        }

    def render_to_html(self,
        template_name="simple_billing/invoice.html",
        extra_context=None,
        **kwargs
        ):
        context = self.get_render_context()
        if extra_context:
            context.update(extra_context)
        return render_to_string(template_name, context, **kwargs)

    def render_to_pdf(self,
        template_name="simple_billing/invoice.html",
        extra_context=None,
        **kwargs
        ):
        context = self.get_render_context()
        if extra_context:
            context.update(extra_context)
        return generate_pdf(template_name, context, **kwargs)

    # def send_email(self):


class Invoice(InvoiceBase):
    pass


class InvoiceItemBase(models.Model):
    invoice = models.ForeignKey(
        app_settings.INVOICE_MODEL,
        related_name="items",
        )
    item = models.TextField(
        _(u"item"),
        blank=True,
        )
    description = models.TextField(
        _(u"description"),
        blank=True
        )
    unit_cost = models.DecimalField(
        _(u"unit_cost"),
        max_digits=app_settings.MAX_DIGITS,
        decimal_places=app_settings.DECIMAL_PLACES,
        blank=True, null=True,
       )
    qty = models.IntegerField(
        _(u"quantity"),
        null=True, blank=True,
        )
    total = models.DecimalField(
        _(u"total"),
        max_digits=app_settings.MAX_DIGITS,
        decimal_places=app_settings.DECIMAL_PLACES,
        )

    class Meta:
        abstract = True

    @property
    def calculated_total(self):
        if self.unit_cost is not None and self.qty is not None:
            return self.unit_cost * self.qty

    @property
    def total_money(self):
        return Money(self.total, self.invoice.currency)


class InvoiceItem(InvoiceItemBase):
    pass
