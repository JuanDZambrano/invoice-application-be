from django.urls import include, path
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
]
