from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import User, UserProfile

# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('email', 'first_name', 'last_name','is_active','is_admin', 'is_staff', 'is_active')
	list_filter = ('is_admin','is_staff',)

	fieldsets = (
			(None, {'fields': ('first_name', 'last_name','email','password')}),
			('Permissions', {'fields': ('is_admin','is_staff', 'is_active')})
		)
	search_fields = ('email','first_name',)
	ordering = ('email', 'is_active')
	
	filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.register(UserProfile)

admin.site.unregister(Group)