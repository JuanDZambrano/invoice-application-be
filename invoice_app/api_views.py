from django.db.models import F, Sum
from django.db.models.functions import Coalesce, ExtractYear, ExtractMonth
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (EmployeeExpense,
                     Sale,
                     Debt,
                     Employee)
from datetime import datetime


class PLStatementView(APIView):
    def get(self, request, format=None):
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        sort_by = request.query_params.get('sort_by', 'profit')

        # Convert dates to datetime objects
        if start_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date is not None:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Apply date filters to queries
        sales = Sale.objects.all()
        debts = Debt.objects.all()
        employees = Employee.objects.all()
        if start_date is not None:
            sales = sales.filter(date__gte=start_date)
            debts = debts.filter(date__gte=start_date)
            employees = employees.filter(date_hired__lte=start_date)
        if end_date is not None:
            sales = sales.filter(date__lte=end_date)
            debts = debts.filter(date__lte=end_date)
            employees = employees.filter(date_hired__lte=end_date)

        # Calculate total revenue
        total_revenue = Sale.objects.filter(date__range=[start_date, end_date]).annotate(
            total_price=F('product__price') * F('quantity')
        ).aggregate(revenue=Sum('total_price'))['revenue'] or 0
        total_debts = debts.aggregate(debts=Sum('amount'))['debts'] or 0

        # Calculate total employee expenses
        total_salaries = Employee.objects.annotate(
            months_worked=ExtractYear(Coalesce('date_terminated', date.today())) - ExtractYear('date_hired') * 12
            + ExtractMonth(Coalesce('date_terminated', date.today())) - ExtractMonth('date_hired')
        ).aggregate(
            total_salaries=Sum(F('wage') * F('months_worked'))
        )['total_salaries'] or 0
        total_extra_expenses = EmployeeExpense.objects.aggregate(
            extra_expenses=Sum('amount'))['extra_expenses'] or 0
        total_employee_expenses = total_salaries + total_extra_expenses

        # Calculate profit
        profit = total_revenue - total_debts - total_employee_expenses

        # Create response data
        data = {
            'total_revenue': total_revenue,
            'total_debts': total_debts,
            'total_employee_expenses': total_employee_expenses,
            'profit': profit,
        }

        # Sort response data
        if sort_by in data:
            data = dict(
                sorted(data.items(), key=lambda item: item[1], reverse=True))

        return Response(data)
