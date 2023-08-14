from django_filters import rest_framework as filters

from .models import (Bill, Category, Customer, Employee, Job, Location, Order,
                     OrderItem, Payment, Product)


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        fields = '__all__'


class LocationFilter(filters.FilterSet):
    class Meta:
        model = Location
        fields = '__all__'


class JobFilter(filters.FilterSet):
    class Meta:
        model = Job
        fields = '__all__'


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = '__all__'


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'


class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = '__all__'


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemFilter(filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = '__all__'


class BillFilter(filters.FilterSet):
    class Meta:
        model = Bill
        fields = '__all__'
