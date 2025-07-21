from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView,TemplateView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Local imports
from ..forms import RegistrationForm
from ..models import User, UserProfile
from ..emails.registration_email import register_email
# from finder.models import Finder, FinderToOwner
# from owner.models import Owner
from ..tokens import account_activation_token

class UserRegistrerView(View):
    """
    
    """
    template_name = 'login/register.html'
    # form_class = UserLoginEmailForm

    def get(self, request, id=None,  **kwargs):
        if request.user.is_authenticated:
            logout(request)
        try:
            print('request.session', request.session['email'], request.session['to_register'])
            # email has to be available and user registered
            if request.session['email'] is None or request.session['to_register'] is False:
                return redirect('accounts:login')
        except KeyError:
            return redirect('accounts:login')
        email = request.session['email']
        try:
            usr = User.objects.get(email=email)
            messages.warning(request, mark_safe(_('Un utilizator cu acest email este inregistrat'
                )))
            return redirect('accounts:auth')
        except User.DoesNotExist:
            pass
        initial={'email':email}
        form = RegistrationForm(initial)
        args = {'form': form, 'email':email}
        return render(request, self.template_name, args )
    
    def post(self, request, id=None,  **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            with transaction.atomic():
                new_user = form.save()
                usr_new = User.objects.get(id=new_user.id)
                message = {
                    'scheme':request.scheme,
                    'current_site': get_current_site(request),
                    'user': new_user.first_name,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.email)),
                    'token':account_activation_token.make_token(new_user),
                    'email_to': form.cleaned_data.get('email'),
                    'mail_subject': 'Confirmare creare cont FactInv',
                }
                try:
                    register_email(message)
                except TimeoutError:
                    messages.error(request, mark_safe(_('Emailul nu a putut fi expediat! Te rog sa ne contacteczi la <strong>0362 100 200</strong>'
                            )))
                messages.success(request, mark_safe(_('Îți mulțumim! Contul a fost creat cu succes. </br> Te rugăm să verifici adresa de e-mail pentru activare.'
                                            'În unele cazuri acest email poate ajunge în directorul <strong>Spam</strong>.'
                )))
                return redirect('accounts:login')
        else:
            return render(request, self.template_name,  {"form": form})
        