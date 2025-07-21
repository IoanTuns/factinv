import imp
from django.contrib import admin
from .models import MyCompany, UsersAndCompany, CurrentCompany
# Register your models here.

class MyCompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("cui",)}
    def save_model(self, request, obj, form, change):
        try:
            print(request.user)
            obj.created_by = request.user
            print(obj.created_by)
            self = super(MyCompany, self).save_model(self, request, obj, form, change)
            print(self.created_by)
            comp = UsersAndCompany.objects.create(user=request.user, company = self.id, created_by=request.user)
            comp.save()
        except IntegrityError as saveException:
            logger.exception('Eroare salvare companie %s...' % self.__class__.__name__)

admin.site.register(MyCompany)
admin.site.register(UsersAndCompany)
admin.site.register(CurrentCompany)