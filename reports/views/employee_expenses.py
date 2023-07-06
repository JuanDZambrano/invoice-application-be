from datetime import datetime

from django.db.models import Sum
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

from invoice_app.models import EmployeeExpense
from reports.serializers import (EmployeeExpenseSerializer,
                                 EmployeeExpensesGroupedSerializer)


class EmployeeExpenseFilter(filters.FilterSet):
    date_gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = EmployeeExpense
        fields = ['date_gte', 'date_lte', 'employee', 'employee__name']


class EmployeeExpensesView(ListAPIView):
    queryset = EmployeeExpense.objects.all()
    serializer_class = EmployeeExpenseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EmployeeExpenseFilter
    search_fields = ['employee__name']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.request.query_params.get('group_by') == 'employee':
            return EmployeeExpensesGroupedSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        group_by_employee = self.request.query_params.get('group_by', None)

        if group_by_employee == 'employee':
            queryset = queryset.values('employee__name').annotate(
                total_expenses=Sum('amount')).order_by('-total_expenses')

        return queryset
