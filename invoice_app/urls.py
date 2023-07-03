from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet,
                    ContactViewSet,
                    SaleViewSet,
                    DebtViewSet,
                    EmployeeViewSet)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'debts', DebtViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
