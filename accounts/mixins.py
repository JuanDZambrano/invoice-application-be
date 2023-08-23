from rest_framework.exceptions import PermissionDenied


class RetrieveOwnDataMixin:
    """
    Mixin to ensure a user can only retrieve their own data.
    """

    def get_object(self):
        obj = self.request.user
        if obj != self.request.user:
            raise PermissionDenied("You can only access your own data.")
        return obj
