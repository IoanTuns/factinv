import os
import string
import random
import datetime

from django.shortcuts import HttpResponse

def base_html(request):
    extended_template = 'base.html'

    if request.user.is_authenticated:
            extended_template = 'base_dashboard.html'
    
    return extended_template

def download(request, file_path, file_name, file_type):
    if os.path.exists(file_path):
        response = HttpResponse(content_type=file_type)
        response['X-Sendfile'] = file_path
        response['Content-Disposition'] = 'attachment; filename=file_name'
        print (response)
        return response
    raise 'File not found'

def default_random():
    size = 24
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(size)])