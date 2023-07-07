from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

from invoice_app.models import Sale
from reports.serializers import GroupedSaleSerializer, SaleSerializer


class SaleFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Sale
        fields = ['date_range', 'product', 'customer']


class CustomOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if 'total_sales' in ordering and 'group_by' in request.query_params:
                return queryset.order_by(*ordering)
            else:
                return queryset.order_by(*ordering)

        return queryset


class SalesView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, CustomOrderingFilter]
    filterset_class = SaleFilter
    search_fields = ['product__name', 'customer__name']
    ordering_fields = ['date', 'quantity', 'total_sales']
    ordering = ['-date']

    def get_serializer_class(self):
        group_by = self.request.query_params.get('group_by', None)
        if group_by:
            return GroupedSaleSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        group_by_fields = self.request.query_params.get('group_by', None)

        if group_by_fields:
            group_by_fields = group_by_fields.split(',')
            # Annotate total_price
            queryset = queryset.annotate(
                total_price=ExpressionWrapper(
                    F('product__price') * F('quantity'),
                    output_field=DecimalField()
                )
            )
            queryset = queryset.values(*group_by_fields).annotate(
                total_sales=Sum('total_price')).order_by('-total_sales')

        return queryset
