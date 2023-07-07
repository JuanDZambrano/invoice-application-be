from django.utils.translation import gettext_lazy as _

# Contact Category Choices
CUSTOMER = 'CU'
PROVIDER = 'PR'
CATEGORY_CHOICES = [
    (CUSTOMER, 'Customer'),
    (PROVIDER, 'Provider'),
]

# Invoice status choices
STATUS_CHOICES = (
    ('draft', _('Draft')),
    ('sent', _('Sent')),
    ('paid', _('Paid')),
    ('overdue', _('Overdue')),
)

PAYMENT_METHOD_CHOICES = (
    ('credit_card', _('Credit Card')),
    ('debit_card', _('Debit Card')),
    ('cash', _('Cash')),
    ('transfer', _('Transfer')),
)
