from datetime import datetime

from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from invoice_app.models import EmployeeExpense
from reports.serializers import (EmployeeExpenseSerializer,
                                 EmployeeExpensesGroupedSerializer)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EmployeeExpensesView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        # Get the 'start_date', 'end_date', 'employee', 'group_by' query parameters
        start_date_str = request.query_params.get('start_date', None)
        end_date_str = request.query_params.get('end_date', None)
        employee_name = request.query_params.get('employee', None)
        group_by_employee = request.query_params.get('group_by', None)

        # Start with all expenses
        queryset = EmployeeExpense.objects.all()

        # If a start date was provided, filter the queryset
        if start_date_str is not None:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(date__gte=start_date)

        # If an end date was provided, filter the queryset
        if end_date_str is not None:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(date__lte=end_date)

        # If an employee name was provided, filter the queryset
        if employee_name is not None:
            queryset = queryset.filter(employee__name__icontains=employee_name)

         # If group_by query parameter is provided and equals 'employee', group by employee
        if group_by_employee == 'employee':
            queryset = queryset.values('employee__name').annotate(
                total_expenses=Sum('amount')).order_by('-total_expenses')
            serializer_class = EmployeeExpensesGroupedSerializer
        else:
            serializer_class = EmployeeExpenseSerializer

        # Apply pagination
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        if paginated_queryset is not None:
            serializer = serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
