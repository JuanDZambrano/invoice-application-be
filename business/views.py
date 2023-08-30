from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.mixins import CompanyFilterMixin

from .constants import BILL_STATUS_CHOICES, BILL_TYPE_CHOICES
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

    @action(detail=False, methods=['GET'], url_path='total-order-value-in-date-range')
    def total_order_value_in_date_range(self, request):
        date_gte = request.query_params.get('date__gte')
        date_lte = request.query_params.get('date__lte')

        if date_gte and date_lte:
            try:
                date_gte = timezone.datetime.strptime(
                    date_gte, '%d-%m-%y').date()
                date_lte = timezone.datetime.strptime(
                    date_lte, '%d-%m-%y').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use dd-mm-yy"}, status=400)

            total_value = OrderItem.objects.filter(
                order__creation_date__gte=date_gte,
                order__creation_date__lte=date_lte
            ).aggregate(Sum('total_price'))

            return Response({"total_value": total_value['total_price__sum']})

        return Response({"error": "Both date__gte and date__lte must be provided"}, status=400)


class BillViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    permission_classes = (CustomUserPermissions,)
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filterset_class = BillFilter

    @action(detail=False, methods=['GET'], url_path='total-bill-value-in-date-range-and-status')
    def total_bill_value_in_date_range_and_status(self, request):
        date_gte = request.query_params.get('date__gte')
        date_lte = request.query_params.get('date__lte')
        bill_status = request.query_params.get('status')
        bill_type = request.query_params.get('type')

        if date_gte and date_lte and bill_status:
            try:
                date_gte = timezone.datetime.strptime(
                    date_gte, '%d-%m-%y').date()
                date_lte = timezone.datetime.strptime(
                    date_lte, '%d-%m-%y').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use dd-mm-yy"}, status=400)

            valid_statuses = [choice[0] for choice in BILL_STATUS_CHOICES]
            if bill_status not in valid_statuses:
                return Response({"error": "Invalid bill status"}, status=400)

            valid_types = [choice[0] for choice in BILL_TYPE_CHOICES]
            if bill_type not in valid_types:
                return Response({"error": "Invalid bill type"}, status=400)

            total_value = Bill.objects.filter(
                due_date__gte=date_gte,
                due_date__lte=date_lte,
                status=bill_status,
                type=bill_type
            ).aggregate(Sum('amount'))

            return Response({"total_value": total_value['amount__sum']})

        return Response({"error": "date__gte, date__lte, and status must all be provided"}, status=400)
