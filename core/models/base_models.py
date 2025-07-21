import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User

class BaseCreateModel(models.Model):
    """
    Abstact class for common model atributes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    created_at = models.DateTimeField(
        verbose_name=(_("Creat la")),
        auto_now_add=True,
    )
    last_change = models.DateTimeField(
        verbose_name=(_("Ultima modificare")),
        auto_now=True,
        )
    is_active = models.BooleanField(
		default=True,
		help_text= _('Modelul de tiparire este disponibil pentru tiparire'),
	)
    
    class Meta:

        abstract = True

class CreatedatModelAdmin(BaseCreateModel):
    """
    Only users with admin rights can create tis model
    """
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={'is_admin': True},
        verbose_name=(_("Creat de")),
    )
    
    class Meta:
        abstract = True
        
class CreatedatModelStaff(BaseCreateModel):
    """
    Only users with admin rights can create tis model
    """
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={'is_staff': True},
        verbose_name=(_("Creat de")),
    )

    class Meta:

        abstract = True

class CreatedatModelUser(BaseCreateModel):
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=(_("Creat de")),
    )
    
    class Meta:

        abstract = True

class UpdateModelUser(BaseCreateModel):
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=(_("Actualizat de")),
    )
    
    class Meta:

        abstract = True
        
class ContactPerson(CreatedatModelUser):
    
    denumire = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text=_("Nume client"),
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
        )
    
    
    class Meta:

        abstract = True