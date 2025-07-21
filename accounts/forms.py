
from django.contrib.auth import get_user_model
from django.db.models import Q
from django import forms

from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from phonenumber_field.formfields import PhoneNumberField

from .models import UserProfile
from . import UserFormErrors
User = get_user_model()


class UserLoginEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        error_messages=UserFormErrors.missing_email,
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError(UserFormErrors.missing_email)
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
                Q(email__iexact=query)
            ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise ValidationError(
                _("Adresa de email si parola introdusa nu se potrivesc. Va rugam sa introduceti datele corecte."), 
                code='error'
                )
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise ValidationError(
                _("Adresa de email si parola introdusa nu se potrivesc. Va rugam sa introduceti datele corecte."), 
                code='error'
                )
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
# class RegistrationForm(forms.Form):
class RegistrationForm(UserCreationForm):    
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)
    is_accsept = forms.BooleanField(
        initial=False, 
        label=_('Accept termeni si conditii.'),
        required=True,
    )
    
    class Meta:
        model = User
        fields = (
			'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_accsept'
        )
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError(_('Un cont este deja creat cu această adresă de email.'
                                    'Pentru a intra in cont acesați sectiunea Autentificare'),
                                code='duplicate_email'
                            )
    def clean_is_accsept(self):
        accsept = self.cleaned_data["is_accsept"]
        if accsept is True:
            return accsept
        else:
            raise ValidationError(_('Pentru a crea contul va rugam sa citiți și să aceptați termeni si condiții'),
                                code='termeni_si_conditii'
                            )

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        is_accsept = self.cleaned_data['is_accsept']
        is_active = False
        is_owner = True
        user = User(
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        is_accsept = is_accsept,
                        is_active = is_active,
                        is_owner = is_owner
                    )
        if commit:
            user.save()
        return user

class UserProfileForm(forms.Form):

    class Meta:
        model = UserProfile
        readonly_fields = ('email')
    
    first_name = forms.CharField(
        widget=forms.TextInput(
        ), 
        label=_('Nume'), 
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
        ),  
        label=_('Prenume'), 
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'readonly':'readonly'}
        ),  
        label=_('Email'), 
    )
    phone_no = PhoneNumberField(
        widget=forms.TextInput(
            ), 
        label=_("Nr de telefon"),
        help_text='doar nr de Romania'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)







