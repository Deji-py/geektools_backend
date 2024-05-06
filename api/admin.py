from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User
from .models import *


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'is_verified','auth_provider']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    ordering = ('email',)





class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'country', 'profile_picture', 'role', 'company', 'date_created', 'date_updated')
    search_fields = ('user__email', 'first_name', 'last_name', 'email')
    list_filter = ('role', 'date_created', 'date_updated')

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user','code')  
    search_fields = ('user__first_name', 'user__last_name', 'code') 





# Register the CustomUser model with the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(OneTimePassword, OneTimePasswordAdmin)
