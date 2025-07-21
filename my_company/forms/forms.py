from pyexpat import model
from django.db.models import Q
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from my_company.models import MyCompany, UsersAndCompany

class MyCompanyCreateForm(forms.ModelForm):
    
    class Meta:
        model = MyCompany
        fields = '__all__'
        exclude = ('created_by', 'slug','is_active')


class MyCompanyUpdateForm(forms.ModelForm):
    cui = forms.CharField(max_length=14, disabled=True)
    
    class Meta:
        model = MyCompany
        fields = '__all__'
        exclude = ('created_by', 'slug','is_active')

class RegisterCompany(forms.ModelForm):
    
    class Meta:
        model=MyCompany
        fields = ('__all__')  
    