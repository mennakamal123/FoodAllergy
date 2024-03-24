from rest_framework import permissions
from users.models import Doctor
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsDoctor(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_patient:
            raise PermissionDenied(self.message)
        return request.user.doctor is not None

        
class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow doctors to create comments.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return request.user.doctor_profile is not None
        except Doctor.DoesNotExist:
            return False

class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff users to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the post or staff users
        return obj.owner == request.user or request.user.is_staff
