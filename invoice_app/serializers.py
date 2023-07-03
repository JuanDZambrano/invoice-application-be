from rest_framework import serializers
from .models import (Product,
                     Contact,
                     Sale,
                     Debt,
                     Employee,
                     EmployeeExpense,)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeExpense
        fields = '__all__'
