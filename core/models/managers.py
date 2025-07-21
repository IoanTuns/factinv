from django.db import models
from django.utils.translation import gettext_lazy as _

class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super(IsActiveManager, self).get_queryset().filter(is_active=True)
    