from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import PLStatementView, invoice_pdf
from .views import (ContactViewSet, DebtViewSet, EmployeeExpenseViewSet,
                    EmployeeViewSet, InvoiceViewSet, ProductViewSet,
                    SaleViewSet)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'debts', DebtViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'employee_expenses', EmployeeExpenseViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pl_statement/', PLStatementView.as_view()),
    path('invoices/<int:pk>/pdf/', invoice_pdf, name='invoice_pdf'),
]
