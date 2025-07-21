import uuid
from django.db import models
# from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.db.models import Q
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from jsonfield import JSONField
from versatileimagefield.fields import VersatileImageField
from phonenumber_field.modelfields import PhoneNumberField

from . import UserEvents

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class UserManager(BaseUserManager):
	
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
        Creates and saves a User with the given email and password.
        """
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(
			email = email, 
			password = password,
			**extra_fields,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		# extra_fields.setdefault('is_admin', False)
		# extra_fields.setdefault('is_staff', False)
		# extra_fields.setdefault('is_active', True)		#User is active
		# extra_fields.setdefault('is_owner', True)		#User is owner
		#
		#----- is_active and is_owner are set by forms.RegistrationForm
		#
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_active', True)
		# extra_fields.setdefault('is_owner', True)
		if extra_fields.get('is_admin') is not True:
			raise ValueError('Superuser must have is_admin=True.')

		return self._create_user(email, password, **extra_fields)

class IsActiveUserManager(BaseUserManager):
    def get_queryset(self):
        return super(IsActiveUserManager, self).get_queryset().filter(is_active=True)
    
class IsNotActiveUserManager(BaseUserManager):
    def get_queryset(self):
        return super(IsNotActiveUserManager, self).get_queryset().filter(is_active=False)

class AllOwnersUserManager(BaseUserManager):
    def get_queryset(self):
        return super(AllOwnersUserManager, self).get_queryset().filter(
            Q(is_owner=True) & 
            Q(is_active=True)
            )
    
class AllStaffUserManager(BaseUserManager):
    def get_queryset(self):
        return super(AllStaffUserManager, self).get_queryset().filter(
            Q(is_staff=True) & 
            Q(is_active=True)
            )

class OnlyOwnersUserManager(BaseUserManager):
    def get_queryset(self):
        return super(OnlyOwnersUserManager, self).get_queryset().filter(
            Q(is_owner=True)&
            Q(is_active=True)
            ).exlude(is_staff=True)
    
class User(AbstractBaseUser):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name=_('email address'),
			error_messages={
        		'unique': _("This email address it is in use."),
			}
		)
	first_name = models.CharField(
		max_length=255,
		blank=False,
		verbose_name=_('first name'),
		help_text=_('User first name'),
	)
	last_name = models.CharField(
		max_length=255,
		blank=False,
		verbose_name=_('last name'),
		help_text=_('User last name'),
	)
	crate_date = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('date joined'),
		help_text=_('date joined'),
		)
	last_change = models.DateTimeField(
		auto_now=True,
		verbose_name=_('last detais change / Has to be implemented'),
		help_text=_('last detais change / Has to be implemented'),
		)
	is_admin = models.BooleanField(
		default=False,
		help_text=_('is the user an admin with superuser rights'),
		)
	is_staff = models.BooleanField(
		default=False,
		help_text=_('is the user allowed to have access to the admin'),
		)
	is_active = models.BooleanField(
		default=False,
		help_text= _('is the user account currently active'),
		)
	is_accsept = models.BooleanField(
		default=False,
		help_text=_('accepted terms and conditions'),
		)

	objects = UserManager()
	active_objects = IsActiveUserManager()
	inactive_objects = IsNotActiveUserManager()
	all_owners = AllOwnersUserManager()
	all_staff = AllStaffUserManager()
	only_owners = OnlyOwnersUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def __str__(self):
		return self.email

	def get_full_name(self):
		'''
        Returns the first_name plus the last_name, with a space in between.
		'''
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
        Returns the short name for the user.
        '''
		return self.first_name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	def email_user(self, subject, message, from_email=None, **kwargs):
		'''
		Sends an email to this User.
		'''
		send_mail(subject, message, from_email, [self.email], **kwargs)


USER_TYPE_CHOICES = (
      (1, 'customer'),
      (2, 'editor'),
      (3, 'technician'),
      (4, 'supervisor'),
      (5, 'admin'),
        )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=50, default='')
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    user_role = models.SmallIntegerField(choices=USER_TYPE_CHOICES, default='1')
    phone = PhoneNumberField(
						blank=True, 
						verbose_name=_('Numar de telefon.'),
						help_text=_('Numarul pe care puteti fi contactat in cazul pierderi bunului.'),
						)
				
    def __str__(self):
        return self.user.email

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        

post_save.connect(create_profile, sender=User)

# @receiver(post_save, sender=User)
# def add_users_to_group(sender, **kwargs):
#    if kwargs.get('created', False):
#        user = kwargs.get('instance')
#        g = Group.objects.get(name='customer')
#        user.group.add(g)

class UserEvent(models.Model):
    """Model used to store events that happened during the user lifecycle."""

    date = models.DateTimeField(default=timezone.now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in UserEvents.CHOICES
        ],
    )
    # parameters = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)
    parameters = JSONField(blank=True, default=dict)
    user = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)

    class Meta:
        ordering = ("date",)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, user={self.user!r})"
