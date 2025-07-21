from django.urls import path, include
from invoice.views import (
    InvoiceDetailView,
    InvoiceCreateView,
    InvoiceListView,
    InvoiceUpdateView,
    DocumentCreateView,
    DocumentListView
    )


app_name = 'invoice'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='home'),
    path('add/', InvoiceCreateView.as_view(), name='add'),
    path('list/', InvoiceListView.as_view(), name='list'),
    path('update/<slug:slug>/', InvoiceUpdateView.as_view(), name='update'),
    path('detail/<slug:slug>/', InvoiceDetailView.as_view(), name='detail'), 
    path('setari/documente/', DocumentListView.as_view(), name='doc_list'),
    path('setari/documente/add/', DocumentCreateView.as_view(), name='doc_add'),
    path('setari/documente/<slug:slug>/', DocumentCreateView.as_view(), name='doc_detail'),
]
