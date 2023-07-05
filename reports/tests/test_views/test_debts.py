from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from invoice_app.models import PROVIDER, Contact, Debt, Product


class DebtsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.provider = Contact.objects.create(
            name='Provider 1',
            category=PROVIDER,
        )
        self.product = Product.objects.create(
            name='Product 1',
            price=100.00
        )
        self.debt = Debt.objects.create(
            product=self.product,
            provider=self.provider,
            date=date.today(),
            amount=100.00,
            due_date=date.today() + timedelta(days=30)
        )

    def test_no_debts(self):
        Debt.objects.all().delete()
        response = self.client.get(reverse('debts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_single_debt(self):
        response = self.client.get(reverse('debts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_multiple_debts(self):
        Debt.objects.create(
            product=self.product,
            provider=self.provider,
            date=date.today(),
            amount=200.00,
            due_date=date.today() + timedelta(days=30)
        )
        response = self.client.get(reverse('debts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_provider(self):
        provider2 = Contact.objects.create(
            name='Provider 2',
            category=PROVIDER,
        )
        Debt.objects.create(
            product=self.product,
            provider=provider2,
            date=date.today(),
            amount=300.00,
            due_date=date.today() + timedelta(days=30)
        )
        response = self.client.get(
            reverse('debts'), {'provider': self.provider.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_product(self):
        product2 = Product.objects.create(
            name='Product 2',
            price=200.00
        )
        Debt.objects.create(
            product=product2,
            provider=self.provider,
            date=date.today(),
            amount=400.00,
            due_date=date.today() + timedelta(days=30)
        )
        response = self.client.get(
            reverse('debts'), {'product': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_due_date(self):
        Debt.objects.create(
            product=self.product,
            provider=self.provider,
            date=date.today(),
            amount=500.00,
            due_date=date.today() + timedelta(days=60)
        )
        response = self.client.get(
            reverse('debts'), {'due_date': date.today() + timedelta(days=30)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering(self):
        response = self.client.get(reverse('debts'), {'ordering': 'amount'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results']
                         [0]['amount'], "{:.2f}".format(self.debt.amount))

    def test_pagination(self):
        for _ in range(20):
            Debt.objects.create(
                product=self.product,
                provider=self.provider,
                date=date.today(),
                amount=100.00,
                due_date=date.today() + timedelta(days=30)
            )
        response = self.client.get(reverse('debts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertTrue('next' in response.data)

    def test_grouping(self):
        provider2 = Contact.objects.create(
            name='Provider 2',
            category=PROVIDER
        )
        Debt.objects.create(
            product=self.product,
            provider=provider2,
            date=date.today(),
            amount=200.00,
            due_date=date.today() + timedelta(days=30)
        )
        response = self.client.get(reverse('debts'), {'group_by': 'provider'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]
                         ['provider__name'], self.debt.provider.name)
        self.assertEqual(response.data['results']
                         [0]['total_debt'], "{:.2f}".format(self.debt.amount))
