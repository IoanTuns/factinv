from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer
from .forms import CustomerCreateForm
# Create your views here.
 

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    # fields= ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    form_class = CustomerCreateForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    # fields= ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    form_class = CustomerCreateForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    fields= ['customer_type','denumire', 'cui', 'judet', 'oras', 'telefon', 'company']
    
    def get_queryset(self):
        return Customer.objects.owne_company_active(self.request.user)