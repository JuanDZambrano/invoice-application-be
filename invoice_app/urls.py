from django.urls import include, path
from invoice_app.api_views import PLStatementView
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet,
                    ContactViewSet,
                    SaleViewSet,
                    DebtViewSet,
                    EmployeeViewSet,
                    EmployeeExpenseViewSet)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'debts', DebtViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'employee_expenses', EmployeeExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pl_statement/', PLStatementView.as_view()),
]
