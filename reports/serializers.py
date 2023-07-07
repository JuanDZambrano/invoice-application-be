from rest_framework import serializers

from invoice_app.models import Debt, EmployeeExpense, Sale


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


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['product', 'customer', 'date', 'quantity', 'total_price']


class GroupedSaleSerializer(serializers.Serializer):
    total_sales = serializers.DecimalField(max_digits=6, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            keys = self.instance[0].keys()
            for key in keys:
                self.fields[key] = serializers.CharField()


class EmployeeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeExpense
        fields = ['employee', 'amount', 'date', 'description']


class EmployeeExpensesGroupedSerializer(serializers.Serializer):
    employee__name = serializers.CharField()
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
