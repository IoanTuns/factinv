from django.http import JsonResponse

# https://www.codingforentrepreneurs.com/blog/ajaxify-django-forms/
class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            return JsonResponse(data, status=200)
        else:
            return response
        
        
    #     class AjaxFormMixin(object):
    # def form_invalid(self, form):
    #     response = super(AjaxFormMixin, self).form_invalid(form)
    #     if self.request.is_ajax():
    #         return JsonResponse(form.errors, status=400)
    #     else:
    #         return response

    # def form_valid(self, form):
    #     response = super(AjaxFormMixin, self).form_valid(form)
    #     if self.request.is_ajax():
    #         print(form.cleaned_data)
    #         data = {
    #             'message': _("Cerere realizata cu succes.")
    #         }
    #         return JsonResponse(data, status=200)
    #     else:
    #         return response