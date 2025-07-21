import uuid
from django.apps import AppConfig


class InvoiceConfig(AppConfig):
    default_auto_field = 'uuid.uuid4'
    name = 'invoice'
