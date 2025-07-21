from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()

@register.filter(is_safe=True)
def js_msg(obj):
    msg={}
    msg_list=[]
    for o in obj:
        msg= o.__dict__
        if msg['level'] == 10:
            msg['level'] = 'debug'
        elif msg['level'] == 20:
            msg['level'] = 'info'
        elif msg['level'] == 25:
            msg['level'] = 'success'
        elif msg['level'] == 30:
            msg['level'] = 'warning'
        elif msg['level'] == 40:
            msg['level'] = 'error'
        msg_list.append(msg)
    return mark_safe(json.dumps(msg_list))
