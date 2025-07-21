from xml.etree.ElementInclude import include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, 
    CreateView, 
    ListView, 
    UpdateView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from extra_views import (
    CreateWithInlinesView, 
    InlineFormSetFactory,
    ModelFormSetView,
    UpdateWithInlinesView,
    NamedFormsetsMixin
    )
from customers.models import Customer
from invoice.models.models import Invoice, Item
from invoice.models.doc_series import (
    DocumentSeries
    )
from invoice.utils import import_name
from invoice.forms import (
    InvoiceCreateForm,
    InvoiceUpdateForm,
    DocumentSeriesCreateForm,
    InvoiceViewForm,
    )
from my_company.models import(
    CurrentCompany,
    MyCompany
    )

class ItemInLine(InlineFormSetFactory):
    model = Item
    fields = ['title', 'quantity', 'unit', 'unit_price', 'discount', 'tax_rate_rel', 'is_vat_included']
    template_name = 'trame/components/invoice/add_item_form.html'
# class ItemInLine(ModelFormSetView):
#     model = Item
#     fields = ['title', 'quantity', 'unit', 'unit_price', 'discount', 'tax_rate_rel', 'is_vat_included']
    
class InvoiceCreateView(LoginRequiredMixin,NamedFormsetsMixin, CreateWithInlinesView):
    model = Invoice
    # fields= ['cui', 'nrRegCom', 'denumire', 'cotaTVA']
    form_class = InvoiceCreateForm
    template_name = 'invoice/invoice_form.html'
    inlines = [ItemInLine,]
    inlines_names = ['Items',]
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.supplier = MyCompany.objects.active_company(self.request.user)
        return super().form_valid(form)
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(**kwargs)
        doc_type = 'INVOICE'
        form.fields['series_rel'].queryset = DocumentSeries.objects.doc_user_type(self.request.user, doc_type=doc_type)
        form.fields['customer_name'].queryset = Customer.objects.owne_company_active(self.request.user)
        return form
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'].fields['customer_name'] = Customer.objects.owne_company_active(self.request.user)
        # return context

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoice/invoices_list.html'
        
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Invoice.objects.owne_invoice_all(self.request.user).order_by('-date_issue','-series', '-number' )

class InvoiceDetailView(DetailView):
    model = Invoice
    success_url: reverse_lazy('invoice:detail')
    # def get_queryset(self):
    #     slug = self.kwargs['slug']
    #     return Invoice.objects.owne_invoice_all(self.request.user).filter(slug=slug)
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active and not request.user.is_superuser:
            return HttpResponseForbidden()
        invoice = get_object_or_404(self.model, slug=kwargs.get('slug', None))
        invoicing_formatter = getattr(settings, 'INVOICING_FORMATTER', 'invoice.formatters.html.BootstrapHTMLFormatter')
        formatter_class = import_name(invoicing_formatter)
        formatter = formatter_class(invoice)
        return formatter.get_response()

class InvoiceUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Invoice
    success_url: reverse_lazy('invoice:update')
    form_class = InvoiceUpdateForm
    inlines = [ItemInLine,]
    inlines_names = ['Items',]
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Invoice.objects.owne_invoice_all(self.request.user).filter(slug=slug)
    

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentSeries
    template_name = 'invoice/doc_no_form.html'
    form_class = DocumentSeriesCreateForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.company = MyCompany.objects.active_company(self.request.user)
        return super().form_valid(form)

class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = DocumentSeries
    success_url: reverse_lazy('invoice:doc_update')
    form_class = InvoiceUpdateForm
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return DocumentSeries.objects.doc_list(self.request.user).filter(slug=slug)
    
class DocumentListView(LoginRequiredMixin, ListView):
    model = DocumentSeries
    template_name = 'invoice/doc_no_list.html'
    
    def get_queryset(self):
        return DocumentSeries.objects.doc_list(self.request.user).order_by('-doc_type','-series', '-star_value' )
    

class ItemFormSetView(ModelFormSetView):
    model = Item
    form_class = InvoiceViewForm
    template_name = 'item_formset.html'