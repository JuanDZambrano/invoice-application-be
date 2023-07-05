from django.urls import path

from .views import DebtsView, EmployeeExpensesView

urlpatterns = [

    path(
        'debts/',
        DebtsView.as_view(),
        name='debts'
    ),

    path(
        'employee-expenses/',
        EmployeeExpensesView.as_view(),
        name='employee-expenses'
    ),
]
