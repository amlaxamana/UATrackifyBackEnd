from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization, FormRegistration

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'role', 'office', 'organization')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('first_name', 'last_name', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name')

admin.site.register(User, UserAdmin)
admin.site.register(FormRegistration)
admin.site.register(Organization)
