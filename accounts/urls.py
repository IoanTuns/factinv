
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from . import views
from .views.login import EmailUserLogin, PasswordUserLogin
from .views.register import UserRegistrerView
from django.contrib.auth.views import (
                    LoginView, 
                    LogoutView,
                    PasswordResetView,
                    PasswordResetDoneView,
                    PasswordResetConfirmView,
                    PasswordResetCompleteView
                    )


app_name = 'accounts'
urlpatterns = [
    path('', views.ViewMyAccount.as_view(), name='myaccount'),
    path('login/', EmailUserLogin.as_view(), name='login'),
    path('email_login/', EmailUserLogin.as_view(), name='email_login'),
    path('auth/', PasswordUserLogin.as_view(), name='auth'),
    # path('loginclass/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register, name='signup'),
    path('register/', UserRegistrerView.as_view(), name='register'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', PasswordResetView.as_view(
                                        # from_email=
                                        template_name= 'login/reset_password.html',
                                        success_url=reverse_lazy('accounts:password_reset_done'),
                                        email_template_name='email/reset_password_email.html'),
                                        name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name= 'login/reset_password_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name= 'login/reset_password_confirm.html', 
                                                                                        success_url=reverse_lazy('accounts:password_reset_complete')
                                                                                        ), name='password_reset_confirm'),
    path('reset-password/compete/', PasswordResetCompleteView.as_view(template_name= 'login/reset_password_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
]