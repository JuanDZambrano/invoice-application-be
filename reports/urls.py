from django.urls import path

from .views import EmployeeExpensesView

urlpatterns = [
    path(
        'employee-expenses/',
        EmployeeExpensesView.as_view(),
        name='employee-expenses'
    ),
]
