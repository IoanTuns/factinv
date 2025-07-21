from django.contrib import admin
from django.urls import path, include
from .views.views import (
    MyCompanyCreateView, 
    MyCompanyUpdateView, 
    MyCompanyDeleteView, 
    UserAndCompListView,
    CurrentCompanyUpdateView,
    CurrentCompanyListView,
    CurrentCompanyCurrentView
    )
from accounts.views.login import EmailUserLogin
from django.urls import path
from core.views.views import HomeView

app_name = 'company'

urlpatterns = [
    path('', EmailUserLogin.as_view(), name='home'),
    path('add/', MyCompanyCreateView.as_view(), name='add'),
    # path('list/', UserAndCompListView.as_view(), name='list'),
    path('list/', CurrentCompanyListView.as_view(), name='list'),
    path('activate/<slug:slug>/', CurrentCompanyUpdateView.as_view(), name='activate'),
    path('current/', CurrentCompanyCurrentView.as_view(), name='current'),
    path('<slug:slug>/', MyCompanyUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', MyCompanyDeleteView.as_view(), name='delete'),
    
]


