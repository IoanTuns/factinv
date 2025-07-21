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
from ..forms import UserLoginEmailForm, UserLoginForm
from ..models import User, UserProfile
# from owner.models import Owner
from ..tokens import account_activation_token
from ..emails.registration_email import register_email

class EmailUserLogin(View):
    """
    Check if email exist into users model.
    If user exist load login page else redirect to 
    new account page
    """
    template_name = 'login/login.html'

    def get(self, request, id=None,  **kwargs):
        if request.user.is_authenticated:
            logout(request)
        form = UserLoginEmailForm()
        args = {'form': form}
        return render(request, self.template_name, args )
    
    def post(self, request, id=None,  **kwargs):
        form = UserLoginEmailForm(request.POST or None)
        #check if valid form
        if form.is_valid():
            #clean input
            email = form.cleaned_data["email"]
            request.session['email'] = email
            #check if email exist
            user_qs_final = User.objects.filter(
				Q(email__iexact=email)
			).distinct()
            if user_qs_final.exists():
                # set a reference for email status
                request.session['to_register'] = False
                return redirect('accounts:auth')
            else:
                # set a reference for email status
                request.session['to_register'] = True
                return redirect('accounts:register')
        else:
            return render(request, self.template_name)
        
class PasswordUserLogin(View):
    """
    Get user email from session and verify and validate 
    the user and passowrd
    """
    template_name = 'login/auth.html'
    def get(self, request, id=None,  **kwargs):
        # one requierd attribute it is missing return to login page
        try:
            # email has to be available and user registered
            if request.session['email'] is None or request.session['to_register'] is True:
                return redirect('accounts:login')
        except KeyError:
            return redirect('accounts:login')
        email = request.session['email']
        try:
            usr = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('accounts:login')
        usr = User.objects.get(email=email)
        name = usr.get_full_name
        initial={'email':email}
        form = UserLoginForm(initial)
        args = {'form': form, 'name':name}
        return render(request, self.template_name, args )
    
    def post(self, request, id=None,  **kwargs):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            # get user object from form
            user_obj = form.cleaned_data.get('user_obj')
            # for active user perform login
            if user_obj.is_active:
                first_login = user_obj.last_login
                login(request, user_obj)
                # perform next redirect if any
                next_redirect = request.POST.get('next')
                if next_redirect is not None:
                    return redirect(next_redirect)
                else:
                    return redirect('accounts:myaccount')
            else:
                message = {
                    'scheme':request.scheme,
                    'current_site': get_current_site(request), 
                    'user': user_obj.first_name,
                    'uid':urlsafe_base64_encode(force_bytes(user_obj.email)),
                    'token':account_activation_token.make_token(user_obj),
                    'email_to': user_obj.email,
                    'mail_subject': 'Confirmare creare cont FactInv.',
                }
                register_email(message)
                messages.info = mark_safe(_( 'Acest cont nu este activ. </br> Te rugăm să verifici adresa de e-mail pentru activare. '
                                    'În unele cazuri acest email poate ajunge în directorul <strong>Spam</strong>.'
                                    ))
                return render(request, 'accounts/login.html', {"form": form})
        print('Form Invalid', form)
        return render(request, self.template_name, {"form": form})