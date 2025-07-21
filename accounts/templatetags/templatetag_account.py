from django import template
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        return False

    return group in user.groups.all()