from __future__ import division  # TODO: refactor
import decimal
import uuid
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.template.defaultfilters import slugify

from decimal import Decimal
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField, BICField
from djmoney.forms.widgets import CURRENCY_CHOICES
from internationalflavor.vat_number import VATNumberField
from model_utils import Choices
from model_utils.fields import MonitorField

from django.conf import settings
from django.core.validators import EMPTY_VALUES, MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Max, Sum

from django.db.models import JSONField

from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _

from invoice.querysets import InvoiceQuerySet, ItemQuerySet
from invoice.taxation import TaxationPolicy
from invoice.taxation.eu import EUTaxationPolicy
from invoice.utils import import_name

from core.models.base_models import ( 
                         BaseCreateModel, 
                         CreatedatModelUser,
                         ContactPerson
                         )
from my_company.models import MyCompany
from customers.models import Customer
from .vat_value import VatValue
from .doc_series import DocumentSeries, DOC_TYPE
from .managers import InvoiceManager

COUNTER_PERIOD = Choices(
    ('DAILY', _('zilnic')),
    ('MONTHLY', _('lunar')),
    ('YEARLY', _('anual'))
)

DUE_DATE = Choices(
    ('15', _(u'15 zile termen de plata')),
    ('30', _(u'30 zile termen de plata')),
    ('45', _(u'45 zile termen de plata')),
    # ('CREDIT_NOTE', _(u'Nota de credit'))
)

STATUS = Choices(
    ('NEW', _(u'nou')),
    ('SENT', _(u'trimis')),
    ('RETURNED', _(u'returnat')),
    ('CANCELED', _(u'anulat')),
    ('PAID', _(u'platita')),
    # ('CREDITED', _(u'credited')),
    # ('UNCOLLECTIBLE', _(u'uncollectible')),
)

PAYMENT_METHOD = Choices(
    ('BANK_TRANSFER', _(u'bank transfer')),
    ('CASH', _(u'cash')),
    ('CASH_ON_DELIVERY', _(u'cash on delivery')),
    ('PAYMENT_CARD', _(u'payment card'))
)

DELIVERY_METHOD = Choices(
    ('PERSONAL_PICKUP', _(u'ridicare personala')),
    ('MAILING', _(u'curier / posta')),
    ('DIGITAL', _(u'digital')),
)


# def default_supplier(attribute_lookup):
#     supplier = getattr(settings, 'INVOICING_SUPPLIER', None)

#     if not supplier:
#         return None

#     lookup_object = supplier
#     for attribute in attribute_lookup.split('.'):
#         lookup_object = lookup_object.get(attribute, None)

#     return lookup_object

# class InvoiceManager(models.Manager):
#     def set_supplier(self, user):
#         return self.get_queryset().filter(current_company__user=user, is_active=True)
    

class Invoice(CreatedatModelUser):
    """
    Model representing Invoice itself.
    It keeps all necessary information described at https://www.gov.uk/vat-record-keeping/vat-invoices
    """
    # Supplier details
    supplier = models.ForeignKey( MyCompany, 
        on_delete=models.CASCADE, verbose_name=_(u'Furnizor'),
        related_name="invoice_to_company",)
    # Customer details
    customer_name = models.ForeignKey( Customer, 
        on_delete=models.CASCADE, verbose_name=_(u'Client'),
        related_name="invoice_to_customer",)
    
    # General information
    type = models.CharField(_(u'tip'), max_length=64, choices=DOC_TYPE, default=DOC_TYPE.INVOICE)
    series_rel = models.ForeignKey( DocumentSeries, 
        on_delete=models.CASCADE, verbose_name=_(u'serie document'),
        related_name="invoice_to_doc_series",)
    series = models.CharField(_(u'serie factura'), max_length=10, blank=True, null= True)
    number = models.DecimalField(_(u'numar facura'), max_digits=5, decimal_places=0, blank=True, null= True)
    status = models.CharField(_(u'status'), choices=STATUS, max_length=64, default=STATUS.NEW)
    related_document = models.CharField(_(u'documente legate'), max_length=100, blank=True)
    note = models.CharField(_(u'note'), max_length=255, blank=True, default=_(u'Multumim!'))
    date_issue = models.DateField(_(u'data emiteri'), default=now)
    date_due = models.DateField(_(u'data scadentei'), help_text=_(u'de achitat pana la'), default=now()+timedelta(days=15))
    # Delivery details
    delivery_method = models.CharField(_(u'mod de livrare'), choices=DELIVERY_METHOD, max_length=64,
        default=DELIVERY_METHOD.PERSONAL_PICKUP)

    # sums (auto calculated fields)
    total = models.DecimalField(_(u'total'), max_digits=10, decimal_places=2,
        blank=True, default=0)
    vat = models.DecimalField(_(u'TVA'), max_digits=10, decimal_places=2,
        blank=True, null=True, default=0)
    slug = models.SlugField()
    # managers
    # objects = InvoiceQuerySet.as_manager()
    objects = InvoiceManager()
    
    class Meta:
        # db_table = 'invoicing_invoices'
        verbose_name = _(u'factura')
        verbose_name_plural = _(u'facturi')
        ordering = ('date_issue', 'series', 'number')
        default_permissions = ('list', 'view', 'add', 'change', 'delete')

    def __str__(self):
        return self.number

    def __unicode__(self):
        return self.number

    @transaction.atomic
    def save(self, **kwargs):
        if self.series in EMPTY_VALUES and self._state.adding is True:
            series_obj = DocumentSeries.objects.filter(company=self.supplier, doc_type=self.type, series=self.series_rel.series)
            self.series = series_obj.values_list('series', flat=True).first()
            self.number = series_obj.values_list('next_value', flat=True).first()
            series_obj.update(last_insert=self.number, next_value=self.number+1)
        if not self.slug:
            self.slug = slugify(str(self.series)+'_'+ str(self.number))
        return super(Invoice, self).save(**kwargs)

    def get_absolute_url(self):
        return getattr(settings, 'INVOICING_INVOICE_ABSOLUTE_URL',
            # lambda invoice: reverse('invoice:detail', args=(invoice.slug,))
            lambda invoice: reverse('invoice:list')
        )(self)

    # @staticmethod
    # def get_next_sequence(type, important_date, number_prefix=None):
    #     """
    #     Returns next invoice sequence based on ``settings.INVOICING_SEQUENCE_GENERATOR``.
    #     """
    #     generator = getattr(settings, 'INVOICING_SEQUENCE_GENERATOR', 'invoice.helpers.sequence_generator')
    #     generator = import_string(generator)
    #     return generator(
    #         type=type,
    #         important_date=important_date,
    #         number_prefix=number_prefix,
    #         counter_period=None,
    #         # related_invoices=related_invoices
    #     )

    def _get_number(self):
        """
        Returns next invoice sequence based on ``settings.INVOICING_NUMBER_FORMATTER``.
        """
        formatter = getattr(settings, 'INVOICING_NUMBER_FORMATTER', 'invoice.helpers.number_formatter')
        formatter = import_string(formatter)
        return formatter(self)

    # def get_tax_rate(self):
    #     customer_country_code = self.customer_country.code if self.customer_country else None
    #     supplier_country_code = self.supplier_country.code if self.supplier_country else None

    #     if self.taxation_policy:
    #         # There is taxation policy -> get tax rate
    #         return self.taxation_policy.get_tax_rate(self.customer_vat_id, customer_country_code, supplier_country_code)
    #     else:
    #         # If there is not any special taxation policy, set default tax rate
    #         return TaxationPolicy.get_default_tax(supplier_country_code)

    # http://www.superfaktura.sk/blog/neplatca-dph-vzor-faktury/
    # def is_supplier_vat_id_visible(self):
    #     is_supplier_vat_id_visible = getattr(settings, 'INVOICING_IS_SUPPLIER_VAT_ID_VISIBLE', None)

    #     if is_supplier_vat_id_visible is not None:
    #         return is_supplier_vat_id_visible(self)

    #     if self.vat is None and self.supplier_country == self.customer_country:
    #         return False

    #     # VAT is not 0
    #     if self.vat != 0 or self.item_set.filter(tax_rate__gt=0).exists():
    #         return True

    #     # VAT is 0, check if customer is from EU and from same country as supplier
    #     is_EU_customer = EUTaxationPolicy.is_in_EU(self.customer_country.code) if self.customer_country else False

    #     return is_EU_customer and self.supplier_country != self.customer_country

    @property
    def vat_summary(self):
        #rates_and_sum = self.item_set.all().annotate(base=Sum(F('qty')*F('price_per_unit'))).values('tax_rate', 'base')
        #rates_and_sum = self.item_set.all().values('tax_rate').annotate(Sum('price_per_unit'))
        #rates_and_sum = self.item_set.all().values('tax_rate').annotate(Sum(F('qty')*F('price_per_unit')))

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('select tax_rate as rate, SUM(quantity*unit_price*(100-discount)/100) as base, ROUND(CAST(SUM(quantity*unit_price*((100-discount)/100)*(tax_rate/100)) AS numeric), 2) as vat from invoice_items where invoice_id = %s group by tax_rate;', [self.pk])

        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    @cached_property
    def has_discount(self):
        if not self.item_set.exists():
            return False

        discounts = list(set(self.item_set.values_list('discount', flat=True)))
        return len(discounts) > 1 or discounts[0] > 0

    @cached_property
    def has_unit(self):
        if not self.item_set.exists():
            return False

        units = list(set(self.item_set.values_list('unit', flat=True)))
        return len(units) > 1 or units[0] != Item.UNIT_EMPTY

    @cached_property
    def max_quantity(self):
        quantity = self.item_set.aggregate(Max('quantity'))
        return quantity.get('quantity__max', 1) if quantity else 0

    @cached_property
    def sum_quantity(self):
        quantity = self.item_set.aggregate(Sum('quantity'))
        return quantity.get('quantity__sum', 1) if quantity else 0

    @cached_property
    def all_items_with_single_quantity(self):
        return self.item_set.count() == self.sum_quantity

    @property
    def subtotal(self):
        sum = 0
        for item in self.item_set.all():
            sum += item.subtotal

        # sum -= Decimal(self.credit)  # subtract credit

        return round(sum, 2)

    @property
    def discount(self):
        sum = 0
        for item in self.item_set.all():
            sum += item.discount_amount
        return round(sum, 2)

    @property
    def discount_percentage(self):
        percentage = 100*self.discount/self.total_without_discount
        return round(percentage, 2)

    @property
    def total_without_discount(self):
        return Decimal(self.total) + self.discount

    def calculate_vat(self):
        if len(self.vat_summary) == 1 and self.vat_summary[0]['vat'] is None:
            return None

        vat = 0
        for vat_rate in self.vat_summary:
            vat += vat_rate['vat'] or 0
        return vat

    def calculate_total(self):
        #total = self.subtotal + self.vat  # subtotal with vat
        total = 0

        for vat_rate in self.vat_summary:
            total += Decimal(vat_rate['base']) + Decimal(vat_rate['vat'] or 0)

        #total *= Decimal((100 - Decimal(self.discount)) / 100)  # subtract discount amount
        # total -= Decimal(self.credit)  # subtract credit
        #total -= self.already_paid  # subtract already paid
        return round(total, 2)

    def __str__(self):
        return (str(self.supplier.denumire) + ', '+ str(self.series)+ ', '+ str(self.number))

class Item(CreatedatModelUser):
    WEIGHT = [(i, i) for i in range(0, 20)]
    UNIT_EMPTY = 'EMPTY'
    UNIT_PIECES = 'PIECES'
    UNIT_HOURS = 'HOURS'
    UNITS = (
        (UNIT_EMPTY, ''),
        (UNIT_PIECES, _(u'buc')),
        (UNIT_HOURS, _(u'ora'))
    )

    invoice = models.ForeignKey(Invoice, verbose_name=_(u'invoice'), on_delete=models.CASCADE)
    title = models.CharField(_(u'Produs/serviciu'), max_length=255, blank=True)
    quantity = models.DecimalField(_(u'cantitate'), max_digits=10, decimal_places=3, default=1)
    unit = models.CharField(_(u'UM'), choices=UNITS, max_length=64, default=UNIT_PIECES)
    unit_price = models.DecimalField(_(u'pret pe bucata'), max_digits=10, decimal_places=2)
    discount = models.DecimalField(_(u'reducere (%)'), max_digits=4, decimal_places=1, default=0)
    tax_rate_rel = models.ForeignKey(VatValue, verbose_name=_(u'Tip TVA %'), on_delete=models.CASCADE)
    tax_rate = models.DecimalField(_(u'TVA (%)'), max_digits=4, decimal_places=1, default=0)
    tag = models.CharField(_(u'tag'), max_length=128,
        blank=True, null=True, default=None)
    is_vat_included = models.BooleanField( #TODO
		default=False,
		help_text=_('include TVA '),
        verbose_name=_(u'include TVA %')
		)
    weight = models.IntegerField(_(u'weight'), choices=WEIGHT, help_text=_(u'ordering'),
        blank=True, null=True, default=0)

    # managers
    objects = ItemQuerySet.as_manager()

    class Meta:
        db_table = 'invoice_items'
        verbose_name = _(u'produs/serviciu')
        verbose_name_plural = _(u'produse / servicii')
        ordering = ('-invoice', 'created_at')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return getattr(settings, 'INVOICING_INVOICE_ITEM_ABSOLUTE_URL', lambda item: '')(self)

    @property
    def subtotal(self):
        subtotal = round(self.unit_price * self.quantity, 2)
        return round(Decimal(subtotal) * Decimal((100 - self.discount) / 100), 2)

    @property
    def discount_amount(self):
        subtotal = round(self.unit_price * self.quantity, 2)
        return round(Decimal(subtotal) * Decimal(self.discount / 100), 2)

    @property
    def vat(self):
        return round(self.subtotal * Decimal(self.tax_rate)/100 if self.tax_rate else 0, 2)

    @property
    def unit_price_with_vat(self):
        tax_rate = self.tax_rate if self.tax_rate else 0
        return round(Decimal(self.unit_price) * Decimal((100 + tax_rate) / 100), 2)

    @property
    def total(self):
        return round(self.subtotal + self.vat, 2)

    def save(self, **kwargs):
        tax_rate_obj = VatValue.objects.filter(id=self.tax_rate_rel.id)
        self.tax_rate =tax_rate_obj.values_list('vat_value', flat=True).first()
        return super(Item, self).save(**kwargs)


from ..signals import *