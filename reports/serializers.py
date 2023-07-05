from rest_framework import serializers

from invoice_app.models import Debt, EmployeeExpense


class DebtSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    provider_name = serializers.CharField(
        source='provider.name', read_only=True)

    class Meta:
        model = Debt
        fields = ['id', 'product_name', 'provider_name',
                  'date', 'amount', 'due_date']


class GroupedDebtSerializer(serializers.Serializer):
    provider__name = serializers.CharField()
    total_debt = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        fields = ['provider__name', 'total_debt']


class EmployeeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeExpense
        fields = ['employee', 'amount', 'date', 'description']


class EmployeeExpensesGroupedSerializer(serializers.Serializer):
    employee__name = serializers.CharField()
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
