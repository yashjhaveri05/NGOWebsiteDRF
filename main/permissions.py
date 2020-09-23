from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class IsAdmin(permissions.BasePermission):
    message: "Not allowed To Access"

    def has_permission(self, request, view):
        if request.user.groups.filter(name='ngo_admin').exists():
            return True
        else:
            return False

class Permit(permissions.BasePermission):
    message: "Not allowed To Access"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False