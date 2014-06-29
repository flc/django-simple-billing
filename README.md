django-simple-billing
=====================


Installation
============

Add to your project's `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    # …
    'simple_billing',
)
```

```python
from simple_billing.views import BillingView, CountriesView

    url(r'^api/billing/$', BillingView.as_view(), name="billing"),
    url(r'^api/countries/$', CountriesView.as_view(), name="countries"),
```

Settings
========

Required settings:
------------------

**`SIMPLE_BILLING_INVOICE_FROM`**

Either specify this setting or override the template `simple_billing/invoice_from.html`.

Example setting:

```python
SIMPLE_BILLING_INVOICE_FROM = (
    "Google Inc.\n"
    "1600 Amphitheatre Parkway\n"
    "Mountain View\n"
    "CA 94043\n"
    "USA\n"
    )
```

**`SIMPLE_BILLING_INVOICE_FILES_DIR`**

Optional settings:
------------------

**`SIMPLE_BILLING_DATA_MODEL`**

Default: `simple_billing.BillingData`

**`SIMPLE_BILLING_INVOICE_MODEL`**

Default: `simple_billing.Invoice`

**`SIMPLE_BILLING_INVOICE_IMG_PATH`**

Path to the logo the appear in the invoice.
Default: empty string which means no logo will appear on the invoice

**`SIMPLE_BILLING_DECIMAL_PLACES`**

Number of decimal places assigned to the MoneyField.

**`SIMPLE_BILLING_MAX_DIGITS`**

Max number of digits assigned to the Moneyfield.

**`SIMPLE_BILLING_DEFAULT_INVOICE_PREFIX`**
