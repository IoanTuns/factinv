import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.contenttypes.models import ContentType
from .base_models import ( 
                         BaseCreateModel, 
                         CreatedatModelUser
                         )
from .contenttypes import get_ContentTypes
    
class ContactPhone ( CreatedatModelUser):
    
    phone = PhoneNumberField( blank=False, 
                        verbose_name=_('Numar de telefon'),
                        help_text=_('Contact phone number'),
                        )

class ContactPerson (CreatedatModelUser):
    
    full_name = models.CharField(
		max_length=255,
		blank=True,
		verbose_name=_('Persona de contact'),
		help_text=_('Persona de contact'),
	)
    email = models.EmailField(
			max_length=255,
            blank=True,
			verbose_name=_('adresa email')
	)
    phone = PhoneNumberField( 
            blank=True, 
            verbose_name=_('Numar de telefon'),
            help_text=_('Contact phone number'),
    )


class CustomerCategory(BaseCreateModel):
     
    category_name = models.CharField(max_length=128)
    asigned_models = models.ManyToManyField(ContentType,limit_choices_to=get_ContentTypes)

# class ContactChoice (CreatedatModelUser):
    
#     choice_name = models.CharField(max_length=128)
#     category = models.ForeignKey(CustomerCategory,on_delete=models.Model)

class PeroanaJuridca(CreatedatModelUser):
     
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
        )
    scopTVA = models.BooleanField(
		default=False,
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    statusTvaIncasare = models.BooleanField(
		default=False,
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    statusSplitTVA= models.BooleanField(
		default=False,
		help_text=_('true -pentru platitor in scopuri de tva / false in cazul in care nu e platitor  in scopuri de TVA la data cautata'),
		)
    cotaTVA = models.DecimalField(
        max_digits=2, 
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
    slug = models.SlugField()
    choices = models.ManyToManyField(CustomerCategory,limit_choices_to=models.Q(assigned_models__model__startswith='peroanajuridca'))
    
    class Meta:
        verbose_name = _('Persoana Juridica')
        verbose_name_plural = _('Persoane Juridice')
        # db_table = "core_"
        
class PeroanaFizica(CreatedatModelUser):
     
    denumire = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text=_("Nume societate"),
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
    codPostal = models.CharField(
        blank=True,
        max_length=10,
        help_text=_("cod postal"),
        )
    choices = models.ManyToManyField(CustomerCategory,limit_choices_to=models.Q(asigned_models__model__startswith='peroanafizica'))
    
    class Meta:
        verbose_name = _('Persoana Fizica')
        verbose_name_plural = _('Persoane Fizice')
        # db_table = "my_company"
        
