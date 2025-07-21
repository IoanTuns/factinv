from pyexpat import model
from django.db.models import Q
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _
from invoice.models.doc_series import (
    DocumentSeries
    )
from .models.models import Invoice


class InvoiceCreateForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('supplier','created_by', 'slug','is_active', 'type', 'series', 'number')
 
 
class InvoiceUpdateForm(forms.ModelForm):
    series = forms.CharField(max_length=10, disabled=True)
    number = forms.DecimalField(decimal_places=0 , disabled=True)
    # seria_si_nr = forms.CharField(max_length=10, disabled=True)
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('supplier','created_by', 'slug','is_active', 'series_rel', 'type')

class InvoiceViewForm(forms.ModelForm):
    series = forms.CharField(max_length=10, disabled=True)
    number = forms.DecimalField(decimal_places=0 , disabled=True)
    # seria_si_nr = forms.CharField(max_length=10, disabled=True)
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('created_by', 'slug','is_active', 'series_rel', 'type')
        

class DocumentSeriesCreateForm(forms.ModelForm):
    
    class Meta:
        model = DocumentSeries
        fields = '__all__'
        exclude = ('company','created_by', 'slug','is_active','last_insert','next_value')
