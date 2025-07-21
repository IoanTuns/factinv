import uuid
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import IntegrityError, transaction
from accounts.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

from phonenumber_field.modelfields import PhoneNumberField
from core.models.base_models import (
    CreatedatModelUser, 
    BaseCreateModel
    )

#TODO https://static.anaf.ro/static/10/Anaf/Informatii_R/doc_WS_V5.txt
#TODO https://www.contzilla.ro/cif-cui-nr-registrul-comertului/
#TODO https://wise.com/gb/iban/romania
#TODO validator cota TVA

class MyCompanyManager(models.Manager):
    def active_company(self, user):
        current_company = CurrentCompany.objects.current_for_user(user=user)
        c_company = current_company.get()
        # return MyCompany instance
        owner_company = MyCompany.objects.get(cui = c_company.current_company.company.cui)
        # owner_company = MyCompany.objects.filter(cui = c_company.current_company.company.cui)
        return owner_company
    

class MyCompany(CreatedatModelUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cui = models.CharField(
        max_length=12,
        blank=False,
        null=False,
        help_text=_("Cod Unic de Inregistrare, codul fiscal"),
        unique=True,
        )
    nrRegCom = models.CharField(
        max_length=40,
        blank=False,
        null=False,
        help_text=_("Numar inregistrare registrul comertului"),
        unique=True,
        )
    denumire = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text=_("Nume societate"),
        )
    judet = models.CharField(
        blank=True,
        max_length=250,
        help_text=_("judet"),
        ) 
    
    oras = models.CharField(
        blank=True,
        max_length=250,
        help_text=_("oras"),
        ) 
    strada = models.CharField(
        blank=True,
        max_length=250,
        help_text=_("strada"),
        ) 
    nr = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("nr"),
        ) 
    bloc = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("bloc"),
        ) 
    ap = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("apartament"),
        ) 
    etaj = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("etaj"),
        )
    telefon = PhoneNumberField( 
        blank=True, 
        verbose_name=_('Numar de telefon'),
        help_text=_('Contact phone number'),
        )
    fax = PhoneNumberField( 
        blank=True, 
        verbose_name=_('Fax'),
        help_text=_('Fax'),
        )
    codPostal = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("cod postal"),
        verbose_name=_('cod postal'),
        )
    scopTVA = models.BooleanField(
		default=False,
        verbose_name=_('platitor TVA'),
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    statusTvaIncasare = models.BooleanField(
		default=False,
        verbose_name=_('TVA la incasare'),
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    statusSplitTVA= models.BooleanField(
		default=False,
        verbose_name=_('split TVA'),
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    cotaTVA = models.DecimalField(
        max_digits=2, 
        decimal_places=0,
        help_text=_('Cota TVA'),
        verbose_name=_('cota de tva'),
    )
    iban = models.CharField(
        blank=True,
        max_length=16,
        help_text=_("Contul Iban"),
        verbose_name=_('contul IBAN'),
        )
    banca = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Banca"),
        verbose_name=_('banca'),
        )
    slug = models.SlugField()
    
    #managers
    
    objects = MyCompanyManager()
    
    class Meta:
        verbose_name = _('Companie')
        verbose_name_plural = _('Companii')
        db_table = "my_company"
    
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.cui)
        
        if self._state.adding is True:
            try:
                with transaction.atomic():
                    new = super(MyCompany, self).save(*args, **kwargs)
                    CurrentCompany.objects.set_inactive(user=self.created_by)
                    UsersAndCompany.objects.create(user=self.created_by, company = self, created_by=self.created_by)
            except IntegrityError:
                handle_exception()
        else:
            new = super(MyCompany, self).save(*args, **kwargs)
        return new
    
    def get_absolute_url(self):
        return reverse('company:update', kwargs={'slug': self.slug})
    
    def get_update_url(self):
        return reverse('company:update', kwargs={'slug': self.slug})
            
    def __str__(self):
        return _('%s, %s')%( self.denumire, self.cui)


# class IsUserCompany(models.Manager):
#     def get_queryset(self):
        
#  Return filtered queryset with user
class CurrentUserManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user, is_active=True)
        
class UsersAndCompany(CreatedatModelUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="user_to_company",
	)
    company = models.ForeignKey(
        MyCompany, 
        on_delete=models.CASCADE,
        related_name="company_to_user",
	)
    
    class Meta:
        verbose_name = _('Compania mea')
        verbose_name_plural = _('Companiile mele')
        db_table = "users_and_company"
        unique_together = ('user', 'company')
    
    def __str__(self):
        return _('%s to %s')%( self.user, self.company)
    
    def save(self, *args, **kwargs):  # new

        if self._state.adding is True:
            try:
                with transaction.atomic():
                    new = super(UsersAndCompany, self).save(*args, **kwargs)
                    CurrentCompany.objects.create(current_company = self, is_current=True)
            except IntegrityError:
                handle_exception()
        else:
            new = super(MyCompany, self).save(*args, **kwargs)
        return new

    #manageres
    objects = CurrentUserManager()


class CurrentCompanyManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(current_company__user=user, is_active=True)
    
    def current_for_user(self, user):
        return self.get_queryset().filter(current_company__user=user, is_active=True, is_current=True)
    
    def other_for_user(self, user):
        return self.get_queryset().filter(current_company__user=user, is_active=True, is_current=False)
    
    def set_inactive(self, user):
        return self.get_queryset().filter(current_company__user=user, is_active=True, is_current=True).update(is_current = False)

class CurrentCompany(BaseCreateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_company = models.OneToOneField(
        UsersAndCompany, 
        on_delete=models.CASCADE,
        related_name="UsersAndCompany",
		)
    is_current = models.BooleanField(
		default=False,
		help_text=_('Comania curenta pe care se lucreaza'),
		)
    slug = models.SlugField()

    class Meta:
        verbose_name = _('Compania curenta')
        verbose_name_plural = _('Companie curenta')
        db_table = "current_company"
    
    def __str__(self):
        return _('%s, %s')%( self.current_company.company.cui, self.current_company.company.denumire )
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.current_company.company.cui)
        
        return super(CurrentCompany, self).save(*args, **kwargs)    
    
    def get_absolute_url(self):
        return reverse('company:active', kwargs={'slug': self.slug})
    
    #manageres
    objects = CurrentCompanyManager()
        