from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from invoice_app.models import Employee, EmployeeExpense


class EmployeeExpensesTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create(
            name='Employee 1',
            date_hired=date.today(),
            wage=1000.00
        )
        self.expense = EmployeeExpense.objects.create(
            employee=self.employee,
            amount=100.00,
            date=date.today(),
            description='Expense 1'
        )

    def test_no_expenses(self):
        EmployeeExpense.objects.all().delete()
        response = self.client.get(reverse('employee-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_single_expense(self):
        response = self.client.get(reverse('employee-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_multiple_expenses(self):
        EmployeeExpense.objects.create(
            employee=self.employee,
            date=date.today(),
            description='Expense 2',
            amount=200.00
        )
        response = self.client.get(reverse('employee-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_employee(self):
        employee2 = Employee.objects.create(
            name='Employee 2',
            date_hired=date.today(),
            wage=1000.00
        )
        EmployeeExpense.objects.create(
            employee=employee2,
            date=date.today(),
            description='Expense 3',
            amount=300.00
        )
        response = self.client.get(reverse('employee-expenses'), {
                                   'employee': self.employee.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_date_range(self):
        EmployeeExpense.objects.create(
            employee=self.employee,
            date=date.today() - timedelta(days=30),
            description='Expense 4',
            amount=400.00
        )
        response = self.client.get(reverse('employee-expenses'), {
                                   'start_date': date.today(), 'end_date': date.today()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering(self):
        response = self.client.get(reverse('employee-expenses'), {
            'ordering': 'amount'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['employee'], self.expense.employee.id)
        self.assertEqual(
            response.data['results'][0]['amount'], "{:.2f}".format(self.expense.amount))

    def test_pagination(self):
        for _ in range(20):
            EmployeeExpense.objects.create(
                employee=self.employee,
                date=date.today(),
                description='Expense',
                amount=100.00
            )
        response = self.client.get(reverse('employee-expenses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertTrue('next' in response.data)

    def test_group_by_employee(self):
        EmployeeExpense.objects.create(
            employee=self.employee,
            date=date.today(),
            description='Expense 2',
            amount=200.00
        )
        response = self.client.get(reverse('employee-expenses'), {
                                   'group_by': 'employee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['employee__name'], self.employee.name)
        self.assertEqual(
            float(response.data['results'][0]['total_expenses']), 300.00)
