# app/templatetags/attr_tags.py

from django import template
from my_company.models import CurrentCompany
register = template.Library()

@register.simple_tag(takes_context=True)
def get_current_company(context):
    user = context['request'].user
    active_company = CurrentCompany.objects.current_for_user(user).values_list('slug')
    active_company = active_company.get()
    if len(active_company)>0:
        return active_company[0]
    else:
        return active_company


@register.inclusion_tag('frame/components/company/current_company.html',takes_context=True)
def get_companies_details(context):
    user = context['request'].user
    active_company = CurrentCompany.objects.current_for_user(user)
    all_other = CurrentCompany.objects.other_for_user(user)   
    # print('get_companies_details',all_other)
    # for com in all_other:
    #     print(com)
    if len(active_company)>0:
        return {'active_company':active_company[0], 'companies': all_other}
    else:
        return {'active_company':active_company, 'companies': all_other}

@register.simple_tag(takes_context=True)
def make_company_current(context, company, *args, **kwargs):
    slug = kwargs['slug']
    user = context['request'].user
    # deactivare current objects
    CurrentCompany.objects.current_for_user(user).update(is_current = False)
    # create a list of companyes of active user
    user_comp_list = CurrentCompany.objects.for_user(user)
    # set current the actual company
    user_comp_list.filter(slug=slug).update(is_current = True)
    # select current company
    actual_comp = user_comp_list.filter(is_current=True)
    return actual_comp