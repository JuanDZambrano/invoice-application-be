from rest_framework import permissions


class CustomUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.user_type == 'AD':
            return True

        if request.user.user_type in ['BM', 'SA']:
            return obj.company == request.user.company

        if request.user.user_type == 'AN':
            return request.method in permissions.SAFE_METHODS and obj.company == request.user.company

        return False
