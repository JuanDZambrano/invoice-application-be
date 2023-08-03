from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response

from config.mixins import CompanyFilterMixin

from .filters import (BillFilter, CategoryFilter, CustomerFilter,
                      EmployeeFilter, JobFilter, LocationFilter, OrderFilter,
                      OrderItemFilter, PaymentFilter, ProductFilter)
from .models import (Bill, Category, Customer, Employee, Job, Location, Order,
                     OrderItem, Payment, Product)
from .permissions import CustomUserPermissions
from .serializers import (BillSerializer, CategorySerializer,
                          CustomerSerializer, EmployeeSerializer,
                          JobSerializer, LocationSerializer,
                          OrderItemSerializer, OrderSerializer,
                          PaymentSerializer, ProductSerializer)


class JobViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter


class EmployeeViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter


class LocationViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_class = LocationFilter


class CustomerViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter


class CategoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class ProductViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class PaymentViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter


class OrderViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter


class OrderItemViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_class = OrderItemFilter

    def list(self, request, *args, **kwargs):
        group_by = request.query_params.get('group_by')
        if group_by == 'order':
            data = (
                OrderItem.objects.values('order')
                .annotate(total_price=Sum('total_price'))
                .order_by('order')
            )
            return Response(data)
        else:
            return super().list(request, *args, **kwargs)


class BillViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filterset_class = BillFilter
