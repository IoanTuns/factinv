from pyexpat import model
from django.db.models import Q
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Customer

class CustomerCreateForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('created_by', 'slug','is_active', 'company')
    
    