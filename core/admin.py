from django.contrib import admin
from .models.currency import CurrencyType

# Register your models here.

admin.site.register(CurrencyType)
# # admin.site.register(ContactChoice)
# admin.site.register(PeroanaJuridca)
# admin.site.register(PeroanaFizica)