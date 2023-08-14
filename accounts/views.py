from rest_framework import permissions, viewsets

from config.mixins import CompanyFilterMixin

from .filters import CompanyFilter, CustomUserFilter
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
