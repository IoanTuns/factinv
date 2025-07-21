from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect
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


# Local imports
from ..forms import UserCreationForm, UserLoginForm, RegistrationForm, UserProfileForm
from ..models import User, UserProfile
# from finder.models import Finder, FinderToOwner
# from owner.models import Owner
from core.global_logic import base_html
from core.views.views import logo_email
from ..tokens import account_activation_token
from django.template.loader import get_template
# from amgasit import settings
from core.mixins.ajax import AjaxFormMixin

def register_email(message):
    """
    TODO: Email validation verification

    This function get messege parateters
    and send activation email with txt and html template
    """
    register_email_plaintext = get_template('email/user_activations_msg.txt')
    register_email_htmly     = get_template('email/user_activations_msg.html')
    kwargs = {
        "uidb64": message['uid'],
        "token": message['token']
    }
    activation_url = reverse("accounts:activate", kwargs=kwargs )
    activate_url = "{0}://{1}{2}".format(message['scheme'], message['current_site'], activation_url)
    sender =('Confirmare factins')
    from_email = 'confirmare.factinv.com'
    username = message['user']
    subject, from_email, to = message['mail_subject'], from_email, message['email_to']
    text_content = register_email_plaintext.render({ 'username': username, 'activate_url': activate_url })
    html_content = register_email_htmly.render({ 'username': username, 'activate_url': activate_url })
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    # from https://samoylov.eu/2016/10/19/sending-html-emails-with-embedded-images-from-django/
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    email_logo = logo_email()
    msg.attach(email_logo)
    msg.send() 

def register(request):
    # TODO: Error on productions
    # TODO: Return an msg and activation link if an existing user try to register
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                new_user = form.save()
                usr_new = User.objects.get(id=new_user.id)
                # If came to register form reporting page use sesions to 
                # # create finder to owner relation
                # if 'is_tag_found' in request.session:
                #     owner = Owner.objects.get(user = new_user)
                #     finder_id = request.session['finder_id']
                #     finder = Finder.objects.get(id = finder_id)
                #     new_finder_to_owner = FinderToOwner(
                #         finder = finder,
                #         owner = owner,
                #     )
                #     new_finder_to_owner.save()
                #     request.session.delete()
                message = {
                    'scheme':request.scheme,
                    'current_site': get_current_site(request),
                    'user': new_user.first_name,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.email)),
                    'token':account_activation_token.make_token(new_user),
                    'email_to': form.cleaned_data.get('email'),
                    'mail_subject': 'Confirmare creare cont am-Gasit.ro.',
                }
                register_email(message)
                messages.success(request, mark_safe(_('Îți mulțumim! Contul a fost creat cu succes. </br> Te rugăm să verifici adresa de e-mail pentru activare.'
                                            'În unele cazuri acest email poate ajunge în directorul <strong>Spam</strong>.'
                )))
                return redirect('accounts:login')
    else:
        # If came to register form reporting page use sesions to 
        # prepopulate the form
        if 'is_tag_found' in request.session:
            email = request.session['email']
            first_name = request.session['first_name']
            last_name = request.session['last_name']
            form = RegistrationForm(
                initial={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
        else:
            form = RegistrationForm()
    args = {'form':form}
    return render(request, 'accounts/registration_page.html', args) 


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        logout(request)

    form = UserLoginForm(request.POST or None)
    if request.GET.get('next'):
        if request.user.is_authenticated is False:
            messages.error(
                request,
                _('Te rugăm să te autentifici. Această sectiune este restricționată.'),
                )
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        if user_obj.is_active:
            first_login = user_obj.last_login
            login(request, user_obj)
            next_redirect = request.POST.get('next')
            if next_redirect is not None:
                return redirect(next_redirect)
            else:
                if first_login is None:
                    # Create first login sesion
                    request.session['is_new'] = True
                    return redirect('accounts:myaccount')
                else:
                    return redirect('owner:dashboard')
        else:
            message = {
                'scheme':request.scheme,
                'current_site': get_current_site(request), 
                'user': user_obj.first_name,
                'uid':urlsafe_base64_encode(force_bytes(user_obj.email)),
                'token':account_activation_token.make_token(user_obj),
                'email_to': user_obj.email,
                'mail_subject': 'Confirmare creare cont am-Gasit.ro.',
            }
            register_email(message)
            msg_reactivate = mark_safe(_( 'Acest cont nu este activ. </br> Te rugăm să verifici adresa de e-mail pentru activare. '
                                'În unele cazuri acest email poate ajunge în directorul <strong>Spam</strong>.'
                                ))
            return render(request, 'accounts/login.html', {"form": form, 'msg_reactivate':msg_reactivate,})
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def change_password(request):
    extended_template = base_html(request)
    title = _('Schimbati parola')
    card_title = _('Schimbati parola')
    card_description = _('Formular schimbare parola')
    submit_action = _('Actualizeaza')
    gargs = {
        'title': title,
        'card_title': card_title,
        'card_description':card_description,
        'submit_action':submit_action,
        }
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts/profile.html')
        else:
            messages.warning(request,
                _('Te rugăm să completezi toate campurile corespunzator')
            )
            form = PasswordChangeForm(user=request.user)
            args = {
                'form': form,
                'extended_template': extended_template,
                'gargs':gargs,
                }

            return render(request, 'accounts/change_password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {
            'form': form,
            'extended_template': extended_template,
            'gargs':gargs,
            }

        return render(request, 'accounts/change_password.html',args)

def activate(request, uidb64, token):
    # Ubuntu 14.04 use a diferent format to pars the key
    lc = len(uidb64)
    if uidb64[0] == 'b' and uidb64[lc-1] == '\'':
        uidb64_strip = uidb64[2:lc-1].strip()
        uidb64 = uidb64_strip
    try:     
        try:
            uid = force_text(urlsafe_base64_decode(uidb64[2:48].strip()))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            if len(uidb64) % 4 != 0: #check if multiple of 4
                while len(uidb64) % 4 != 0:
                    uidb64 += '='
                uid = force_text(urlsafe_base64_decode(uidb64))
            else:
                uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except TypeError:
        user = None
        return HttpResponse('TypeError'+uidb64)
    except ValueError:
        user = None
        return HttpResponse('ValueError'+uidb64)
    except OverflowError:
        user = None
        return HttpResponse('OverflowError'+uidb64)
    except User.DoesNotExist:
        user = None
        return HttpResponse('Utilizator invalid!'+uidb64)
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(
            request,
            _('Mulțumim pentru confirmare. Contul tău este activ.'),
            )
        return redirect('accounts:login')
    else:
        #TODO: pagina de eroare pentru link de activare invalid
        return HttpResponse('Activation link is invalid!')
    

class ViewMyAccount(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_profile.html'
    readonly_fields = 'email'
    title = _('Profilul meu')
    card_title = _('Profilul meu')
    card_description = _('Editatare informații utilizator')
    submit_action = _('Actualizează')
    new_user_msg = () 
    msg = mark_safe(_('Te rugăm să completezi toate datele de profil pentru a putea fi contactat în cazul în care pierdeti un bun înregistrat')
                        )
    gargs = {
        'title': title,
        'card_title': card_title,
        'card_description':card_description,
        'submit_action':submit_action,
        'new_user_msg':new_user_msg,
        }

    def get(self, request):
        user = request.user
        extended_template = base_html(request)

        if hasattr(request.session,'is_new'):
            if request.session['is_new'] is True:
                self.gargs['new_user_msg'] = self.msg
        try:
            user_details = User.objects.get(email=user)
            user_profile = UserProfile.objects.get(user__email=user)
            first_name = user_details.first_name
            last_name = user_details.last_name
            email = user_details.email
            phone_no = user_profile.phone
            if not phone_no:
                self.gargs['new_user_msg'] = self.msg
            else:
                self.gargs['new_user_msg'] = ''
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user_id=user_details.id)
        
        initial = {
            'first_name':first_name,
            'last_name':last_name,
            'email': email,
            'phone_no': phone_no,
        }
        form = UserProfileForm(initial=initial)
        args = {
            'form': form,
            'title': self.title,
            'extended_template': extended_template,
            'gargs':self.gargs,
            }
        return render(request, self.template_name, args )

    def post(self, request):
        form = UserProfileForm(request.POST)
        extended_template = base_html(request)
        if request.user.is_authenticated and '_update_profile' in self.request.POST:
            if form.is_valid():
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                phone_no=form.cleaned_data["phone_no"]
                
                user = User.objects.get(email=request.user.email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.phone = phone_no
                user_profile.save()
                try:
                    if request.session['is_new'] is True:
                        request.session['is_new']= False
                except KeyError:
                    pass
                if not phone_no:
                    self.gargs['new_user_msg'] = self.msg
                else:
                    self.gargs['new_user_msg'] = ''
            args = {
                'form': form, 
                'title': self.title,
                'extended_template': extended_template,
                'gargs':self.gargs,
                }
            return render(request, self.template_name, args)
        

    def get_absolute_url(self):
        return reverse('accounts:myaccount')
