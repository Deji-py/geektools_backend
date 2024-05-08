from rest_framework import permissions
from datetime import datetime, timedelta
from django.utils import timezone




class IsFreemium(permissions.BasePermission):
    #Permission to check if the user is a member of the 'vendor' group.
    message = "This user can't access the page"

     #Check if the user belongs to the 'vendor' group.
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Freemium').exists():
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        


class IsPremium(permissions.BasePermission):
    #Permission to check if the user is a member of the 'vendor' group.
    message = "This user can't access the page"

     #Check if the user belongs to the 'vendor' group.
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Premium').exists():
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True