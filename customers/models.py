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


# class ContactChoice (models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
#     choice_name = models.CharField(max_length=128)
#     category = models.ForeignKey(CustomerCategory,on_delete=models.Model)

CUSTOMER_TYPE_CHOICES = (
        ('F',_('Persona Fizica')),
        ('B',_('Persoana Juridica'))
        )

class CustomerManager(models.Manager):
    def owne_company_active(self, user):
        current_company = CurrentCompany.objects.current_for_user(user)
        c_company = current_company.get()
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        return self.get_queryset().filter(company=owner_company, is_active=True)
    
    def owne_company_all(self, company):
        return self.get_queryset().filter(company=company)

class Customer(ContactPerson):

    company = models.ForeignKey(MyCompany, 
        on_delete=models.CASCADE,
        related_name="customer_to_company",)
        
    customer_type = models.CharField(
        max_length=1, 
        choices=CUSTOMER_TYPE_CHOICES, 
        help_text=_('Tip client'),
    )
    cui = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        help_text=_("Cod Unic de Inregistrare, codul fiscal"),
        unique=True,
        )
    nrRegCom = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        help_text=_("Numar inregistrare registrul comertului"),
        unique=True,
        )
    scopTVA = models.BooleanField(
		default=False,
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    cotaTVA = models.DecimalField(
        max_digits=2, 
        blank=True,
        null=True,
        decimal_places=0,
        help_text=_('Cota TVA'),
    )
    iban = models.CharField(
        blank=True,
        max_length=16,
        help_text=_("Contul Iban"),
        )
    banca = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Banca"),
        )
    # slug = models.SlugField()
    
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clienți')
        
    def get_absolute_url(self):
        return reverse('customer:update', kwargs={'pk': self.id})
    
    def get_update_url(self):
        return reverse('customer:update', kwargs={'pk': self.id})
            
    def __str__(self):
        if self.customer_type == 'F':
            self.slug = self.denumire + ', '+ self.oras+', '+self.judet
        elif self.customer_type == 'B':
            self.slug = self.cui+', '+self.denumire
        return _('%s, %s')%( self.denumire, self.cui)
    
    #manageres
    objects = CustomerManager()
    
    def save(self, *args, **kwargs):  # new
        current_company = CurrentCompany.objects.current_for_user(self.created_by)
        print('current_company',current_company)
        c_company = current_company.get()
        print('c_company',c_company)
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        print('owner_company',owner_company)
        # return self.get_queryset().filter(company=owner_company, is_active=True)
        self.company = owner_company
        print('self.company',self.company)
        return super(Customer, self).save(*args, **kwargs)    