from rest_framework import viewsets

from .models import (Contact, Debt, Employee, EmployeeExpense, Invoice,
                     Product, Sale)
from .serializers import (ContactSerializer, DebtSerializer,
                          EmployeeExpenseSerializer, EmployeeSerializer,
                          InvoiceSerializer, ProductSerializer, SaleSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeExpenseViewSet(viewsets.ModelViewSet):
    queryset = EmployeeExpense.objects.all()
    serializer_class = EmployeeExpenseSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
