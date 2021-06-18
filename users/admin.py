from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group


class UserAdminManager(UserAdmin):
    list_display = [f.name for f in User._meta.fields]

    fieldsets = (
        ('Contact info', {'fields': ('email', 'phone',)}),
        ('Details',
         {'fields': (
             'username', 'full_name', 'user_type', 'delivery_address', 'location', 'operation_radius', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = ((None, {
        'fields': (
            'full_name', 'phone', 'email', 'password1', 'password2', 'is_superuser', 'is_staff',
            'is_active')}
                      ),)


admin.site.unregister(Group)
admin.site.register(User, UserAdminManager)
