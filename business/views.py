from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .filters import (BillFilter, CategoryFilter, CustomerFilter,
                      EmployeeFilter, JobFilter, LocationFilter, OrderFilter,
                      OrderItemFilter, PaymentFilter, ProductFilter)
from .mixins import CompanyFilterMixin
from .models import (Bill, Category, Customer, Employee, Job, Location, Order,
                     OrderItem, Payment, Product)
from .serializers import (BillSerializer, CategorySerializer,
                          CustomerSerializer, EmployeeSerializer,
                          JobSerializer, LocationSerializer,
                          OrderItemSerializer, OrderSerializer,
                          PaymentSerializer, ProductSerializer)


class JobViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter
    permission_classes = [permissions.DjangoModelPermissions]


class EmployeeViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    permission_classes = [permissions.DjangoModelPermissions]


class LocationViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_class = LocationFilter
    permission_classes = [permissions.DjangoModelPermissions]


class CustomerViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter
    permission_classes = [permissions.DjangoModelPermissions]


class CategoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    permission_classes = [permissions.DjangoModelPermissions]


class ProductViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [permissions.DjangoModelPermissions]


class PaymentViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    permission_classes = [permissions.DjangoModelPermissions]


class OrderViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    permission_classes = [permissions.DjangoModelPermissions]


class OrderItemViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_class = OrderItemFilter
    permission_classes = [permissions.DjangoModelPermissions]

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
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filterset_class = BillFilter
    permission_classes = [permissions.DjangoModelPermissions]
