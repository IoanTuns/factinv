from django import forms

class HomeForm(forms.Form):
   text = 'Referinta pentru meniuri'

class LoadLogo(forms.Form):
    logo = 'logo.html'