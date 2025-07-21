import decimal
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from django.db import models

from django.utils.translation import gettext_lazy as _

from core.models.base_models import ( 
                         BaseCreateModel
                         )

class VatValue(BaseCreateModel):
    
    vat_value = models.DecimalField(_(u'TVA'), max_digits=3, decimal_places=0, default=19)
    short_desc = models.CharField(_(u'descriere'), max_length=10, blank=True)
    description = models.CharField(_(u'descriere'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _(u'TVA')
        verbose_name_plural = _(u'TVA')
        
    def __str__(self):
        return (str(self.vat_value)+ ', '+ self.short_desc)
