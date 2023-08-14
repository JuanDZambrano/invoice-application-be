from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BillViewSet, CategoryViewSet, CustomerViewSet,
                    EmployeeViewSet, JobViewSet, LocationViewSet,
                    OrderItemViewSet, OrderViewSet, PaymentViewSet,
                    ProductViewSet)

router = DefaultRouter()
router.register('employee', EmployeeViewSet)
router.register('location', LocationViewSet)
router.register('job', JobViewSet)
router.register('customer', CustomerViewSet)
router.register('category', CategoryViewSet)
router.register('product', ProductViewSet)
router.register('payment', PaymentViewSet)
router.register('order', OrderViewSet)
router.register('orderitem', OrderItemViewSet)
router.register('bill', BillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
