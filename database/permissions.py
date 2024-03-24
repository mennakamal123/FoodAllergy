from rest_framework import permissions

class FoodPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve']:
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.user.is_staff
        return False
        
class AllergyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve']:
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.user.is_staff
        return False
    
class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve']:
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.user.is_staff
        return False



class FoodAllergyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve']:
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.user.is_staff
        return False
    
class MiniFoodAllergyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve']:
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.user.is_staff
        return False
