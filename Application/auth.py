# appname/permissions.py
from rest_framework import permissions
from .models import Tenant

class IsCompanyAPIKeyValid(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_AUTHORIZATION')  # Replace with the actual header key
        if api_key:
            try:
                company = Tenant.objects.get(tenant_key=api_key)
                request.company = company  # Store the company object in the request for later use
                return True  # API key is valid, grant permission
            except Tenant.DoesNotExist:
                pass  # API key is not valid, permission denied
        return False  # API key is missing, permission denied
class IsAdminAPIKeyValid(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_AUTHORIZATION')  # Replace with the actual header key
        if api_key:
            try:
                company = Tenant.objects.get(tenant_key=api_key,model_name="admin")
                request.company = company  # Store the company object in the request for later use
                return True  # API key is valid, grant permission
            except Tenant.DoesNotExist:
                pass  # API key is not valid, permission denied
        return False  # API key is missing, permission denied
