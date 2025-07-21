from __future__ import division  # TODO: refactor
import decimal
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

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
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from invoice.querysets import InvoiceQuerySet, ItemQuerySet
from invoice.taxation import TaxationPolicy
from invoice.taxation.eu import EUTaxationPolicy
from invoice.utils import import_name

from core.models.base_models import ( 
                         BaseCreateModel, 
                         CreatedatModelUser,
                         ContactPerson)

from my_company.models import (
    MyCompany,
    CurrentCompany
    )


DOC_TYPE = Choices(
    ('INVOICE', _(u'Factura')),
    # ('ADVANCE', _(u'Advance invoice')),
    ('PROFORMA', _(u'Proforma')),
    ('RECEIPT', _(u'chitata'))
)

class DocumentManager(models.Manager):
    def doc_user_type(self, user, doc_type):
        current_company = CurrentCompany.objects.current_for_user(user=user)
        c_company = current_company.get()
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        active_doc =  self.get_queryset().filter(company=owner_company, is_active=True, doc_type=doc_type)
        return active_doc
    
    def doc_list(self, user):
        owner_company = MyCompany.objects.active_company(user=user)
        active_doc =  self.get_queryset().filter(company=owner_company, is_active=True)
        return active_doc

class DocumentSeries(BaseCreateModel):
    company = models.ForeignKey( MyCompany, 
        on_delete=models.CASCADE, verbose_name=_(u'firma'),
        related_name="invoice_series_to_company",)
    doc_type = models.CharField(_(u'tip document'), max_length=64, choices=DOC_TYPE, default=DOC_TYPE.INVOICE)
    series = models.CharField(_(u'serie document'), max_length=10, blank=True)
    star_value = models.DecimalField(_(u'Primul numar'), max_digits=5, decimal_places=0, default=1)
    end_value = models.DecimalField(_(u'Ultimul numar'), max_digits=5, decimal_places=0, default=99999)
    last_insert = models.DecimalField(_(u'Ultimul introdus'), max_digits=5, decimal_places=0, default=0)
    next_value = models.DecimalField(_(u'Urmatorul'), max_digits=5, decimal_places=0, default=1)
    slug = models.SlugField()
    
    #managers
    objects = DocumentManager()
    
    class Meta:
        verbose_name = _(u'Serie document')
        verbose_name_plural = _(u'Serie documente')
        unique_together = ('company', 'series', 'doc_type', 'star_value')
        
    def __str__(self):
        return (str(self.series)+ ', '+ str(self.star_value) + ', '+ str(self.end_value))
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(str(self.company.cui)+', '+str(self.series)+ ', '+ str(self.star_value) + ', '+ str(self.end_value))
        return super(DocumentSeries, self).save(*args, **kwargs)   
    
    def get_absolute_url(self):
        return reverse('invoice:doc_list')
    