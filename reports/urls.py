from django.urls import path

from .views import DebtsView, EmployeeExpensesView, SalesView

urlpatterns = [
    path(
        'debts/',
        DebtsView.as_view(),
        name='debts'
    ),
    path(
        'sales/',
        SalesView.as_view(),
        name='sales'
    ),
    path(
        'employee-expenses/',
        EmployeeExpensesView.as_view(),
        name='employee-expenses'
    ),
]
