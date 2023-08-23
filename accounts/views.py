from dj_rest_auth.views import LogoutView as DefaultLogoutView
from rest_framework import generics, permissions, viewsets

from config.mixins import CompanyFilterMixin

from .filters import CompanyFilter, CustomUserFilter
from .mixins import RetrieveOwnDataMixin
from .models import Company, CustomUser
from .serializers import CompanySerializer, CustomUserSerializer


class CompanyViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [permissions.DjangoModelPermissions]


class CustomUserViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_class = CustomUserFilter
    permission_classes = [permissions.DjangoModelPermissions]


class LogoutView(DefaultLogoutView):
    def logout(self, request):
        response = super().logout(request)
        response.delete_cookie('app-auth')
        return response


class RetrieveOwnUserDataView(RetrieveOwnDataMixin, generics.RetrieveAPIView):
    """
    View to allow a user to retrieve their own data.
    """
    serializer_class = CustomUserSerializer
    permission_classes = []

    def get_object(self):
        if self.request.user.is_anonymous:
            return None
        return self.request.user
