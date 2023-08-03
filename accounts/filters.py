import django_filters

from .models import Company, CustomUser


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = '__all__'


class CustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = '__all__'
