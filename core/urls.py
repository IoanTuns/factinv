from django.contrib import admin
from django.urls import path, include
from .views.views import HomeView, cookie_policy
from .views.dashboard import UserDashboadView
from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard', UserDashboadView.as_view(), name='dash'),
    path('politica_de_cookie', cookie_policy, name='cookie'),
]


