from django import template

register = template.Library()

# @register.filter
# def nice_iban(iban):
#     return ' '.join(iban[i:i+4] for i in range(0, len(iban), 4))
