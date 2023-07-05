from datetime import datetime

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

from invoice_app.models import Debt
from reports.serializers import DebtSerializer, GroupedDebtSerializer


class DebtsView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'provider', 'due_date', 'amount']
    search_fields = ['product__name', 'provider__name']
    ordering_fields = ['due_date', 'amount']
    ordering = ['-due_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        overdue = self.request.query_params.get('overdue', None)
        group_by_provider = self.request.query_params.get('group_by', None)

        if overdue is not None:
            if overdue.lower() == 'true':
                queryset = queryset.filter(due_date__lt=datetime.now().date())
            else:
                queryset = queryset.filter(due_date__gte=datetime.now().date())

        if group_by_provider is not None and group_by_provider.lower() == 'provider':
            queryset = queryset.values('provider__name').annotate(
                total_debt=Sum('amount')).order_by('-total_debt')

        return queryset

    def get_serializer_class(self):
        group_by_provider = self.request.query_params.get('group_by', None)
        if group_by_provider is not None and group_by_provider.lower() == 'provider':
            return GroupedDebtSerializer
        return DebtSerializer
