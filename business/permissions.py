from rest_framework import permissions


class CustomUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.user_type == 'AD':
            return True

        if request.user.user_type == 'BM':
            return request.user.company == view.kwargs.get('company')

        if request.user.user_type in ['SA', 'AN']:
            return view.action in ['list', 'retrieve']

        return False

    def has_object_permission(self, request, view, obj):
        import pdb
        pdb.set_trace()
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.user_type == 'AD':
            return True

        if request.user.user_type == 'BM':
            return view.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'delete'] and obj.company == request.user.company

        if request.user.user_type == 'SA':
            if view.action in ['list', 'retrieve', 'create', 'partial_update']:
                return obj.company == request.user.company
            elif view.action in ['update', 'partial_update']:
                return obj.company == request.user.company

        if request.user.user_type == 'AN':
            return view.action in ['list', 'retrieve'] and obj.company == request.user.company

        return False
