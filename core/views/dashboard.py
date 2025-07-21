from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from email.mime.image import MIMEImage
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins.ajax import AjaxFormMixin

# Create your views here.


class UserDashboadView(LoginRequiredMixin, AjaxFormMixin, TemplateView):
    template_name = 'dashboard/main_d.html'
    title = _('Contul meu')
    card_title = _('Contul meu')
    card_description = _('Selectați din listă TAGul care a fost pierdut')
    submit_action = _('Cauta')
    link_title = _('Vezi lista completă')
    gargs = {
        'title': title,
        'card_title': card_title,
        'card_description':card_description,
        'submit_action':submit_action,
        'link_title': link_title,
        }
