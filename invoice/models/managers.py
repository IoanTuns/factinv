from operator import mod
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core.models.base_models import ( 
                         BaseCreateModel, 
                         CreatedatModelUser
                         )
from accounts.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from core.models.base_models import ContactPerson
from my_company.models import (MyCompany, CurrentCompany)

class InvoiceManager(models.Manager):
    def owne_invoice_active(self, user):
        current_company = CurrentCompany.objects.current_for_user(user)
        c_company = current_company.get()
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        return self.get_queryset().filter(supplier=owner_company, is_active=True)
    
    def owne_invoice_all(self, user):
        current_company = CurrentCompany.objects.current_for_user(user)
        c_company = current_company.get()
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        return self.get_queryset().filter(supplier=owner_company)