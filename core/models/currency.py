from locale import currency
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base_models import ( 
                         BaseCreateModel, 
                         CreatedatModelUser
                         )

class CurrencyType(BaseCreateModel):
    currency_type = models.CharField(
		max_length=3,
		blank=False,
	)
