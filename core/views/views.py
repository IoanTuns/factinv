from django.views.generic import View
from django.shortcuts import render, redirect
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders

from ..forms import HomeForm
from ..global_logic import base_html

# Create your views here.


def logo_email():
    with open(finders.find('email_img/logo_email.png'), 'rb') as f: 
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dash')
        else:
            return redirect('accounts:login')

def cookie_policy(request):
    return render(request, 'cookies/cookie_policy.html')