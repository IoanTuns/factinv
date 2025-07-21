from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from my_company.forms.forms import MyCompanyCreateForm, MyCompanyUpdateForm
from my_company.models import MyCompany,UsersAndCompany, CurrentCompany

class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    model = MyCompany
    # fields= ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    form_class = MyCompanyCreateForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    # fields: ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    
class MyCompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = MyCompany
    # fields= ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    form_class =  MyCompanyUpdateForm

    
class MyCompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = MyCompany
    success_url = reverse_lazy('company-list')

class UserAndCompListView(LoginRequiredMixin, ListView):
    model = UsersAndCompany
    fields= ['companie']

    def get_queryset(self):
        queryset = UsersAndCompany.objects.filter(user=self.request.user)
        return queryset
    
class CurrentCompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = CurrentCompany
    fields= ['is_active']
    success_url: reverse_lazy('core:home')
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        # deactivare current objects
        CurrentCompany.objects.current_for_user(self.request.user).update(is_current = False)
        # create a list of companyes of active user
        user_comp_list = CurrentCompany.objects.for_user(self.request.user)
        # set current the actual company
        user_comp_list.filter(slug=slug).update(is_current = True)
        # select current company
        actual_comp = user_comp_list.filter(is_current=True)
        return actual_comp
        # return HttpResponseRedirect(reverse('core:home'))
        
class CurrentCompanyCurrentView(LoginRequiredMixin, ListView):
    model = CurrentCompany
    fields= ['current_company']
    
    def get_queryset(self):
        # create a list of companyes of active user
        # user_comp_list = CurrentCompany.objects.for_user(self.request.user).filter(is_current=True)
        # actual_comp = user_comp_list.filter(is_current=True)
        return CurrentCompany.objects.for_user(self.request.user).filter(is_current=True)
    
class CurrentCompanyListView(LoginRequiredMixin, ListView):
    model = CurrentCompany
    fields= ['current_company']
    
    def get_queryset(self):
        return CurrentCompany.objects.for_user(self.request.user)