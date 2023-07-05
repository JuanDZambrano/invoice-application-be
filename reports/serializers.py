from rest_framework import serializers

from invoice_app.models import EmployeeExpense


class EmployeeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeExpense
        fields = ['employee', 'amount', 'date', 'description']


class EmployeeExpensesGroupedSerializer(serializers.Serializer):
    employee__name = serializers.CharField()
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
