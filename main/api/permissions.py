from rest_framework import permissions

class IsNurse(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the role 'nurse'.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the role 'nurse'
        if request.user and request.user.is_authenticated:
            return request.user.role == 'nurse'
        return False
