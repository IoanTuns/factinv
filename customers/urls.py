from django.contrib import admin
from django.urls import path, include
from accounts.views.login import EmailUserLogin
from django.urls import path
from core.views.views import HomeView
from .views import (CustomerCreateView, CustomerUpdateView, CustomerListView)
app_name = 'customer'

urlpatterns = [
    path('', CustomerListView.as_view(), name='home'),
    path('add/', CustomerCreateView.as_view(), name='add'),
    # # path('list/', UserAndCompListView.as_view(), name='list'),
    path('list/', CustomerListView.as_view(), name='list'),
    # path('activate/<slug:slug>/', CurrentCompanyUpdateView.as_view(), name='activate'),
    # path('current/', CurrentCompanyCurrentView.as_view(), name='current'),
    path('<str:pk>/', CustomerUpdateView.as_view(), name='update'),
    # path('<slug:slug>/delete/', MyCompanyDeleteView.as_view(), name='delete'),
    
]