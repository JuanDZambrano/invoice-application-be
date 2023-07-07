from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from invoice_app.models import CUSTOMER, Contact, Product, Sale


class SalesTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product 1', price=100.00)
        self.customer = Contact.objects.create(
            name='Customer 1', category=CUSTOMER)
        self.customer2 = Contact.objects.create(
            name='Customer 2', category=CUSTOMER)
        self.sale = Sale.objects.create(
            product=self.product, customer=self.customer, date=date.today(), quantity=1)

    def test_no_sales(self):
        Sale.objects.all().delete()
        response = self.client.get(reverse('sales'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_single_sale(self):
        response = self.client.get(reverse('sales'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_group_by_product(self):
        response = self.client.get(reverse('sales'), {'group_by': 'product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['product'], str(self.product.pk))

    def test_group_by_customer(self):
        response = self.client.get(reverse('sales'), {'group_by': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['customer'], str(self.customer.pk))

    def test_group_by_date(self):
        response = self.client.get(reverse('sales'), {'group_by': 'date'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['date'], str(self.sale.date))

    def test_group_by_product_and_customer(self):
        response = self.client.get(
            reverse('sales'), {'group_by': 'product,customer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['product'], str(self.product.pk))
        self.assertEqual(response.data['results']
                         [0]['customer'], str(self.customer.pk))

    def test_group_by_product_and_date(self):
        response = self.client.get(
            reverse('sales'), {'group_by': 'product,date'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['product'], str(self.product.pk))
        self.assertEqual(response.data['results']
                         [0]['date'], str(self.sale.date))

    def test_group_by_customer_and_date(self):
        response = self.client.get(
            reverse('sales'), {'group_by': 'customer,date'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['customer'], str(self.customer.pk))
        self.assertEqual(response.data['results']
                         [0]['date'], str(self.sale.date))

    def test_group_by_product_customer_and_date(self):
        response = self.client.get(
            reverse('sales'), {'group_by': 'product,customer,date'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['product'], str(self.product.pk))
        self.assertEqual(response.data['results']
                         [0]['customer'], str(self.customer.pk))
        self.assertEqual(response.data['results']
                         [0]['date'], str(self.sale.date))

    def test_ordering_by_total_sales(self):

        Sale.objects.create(
            product=self.product,
            customer=self.customer,
            date=date.today(),
            quantity=10
        )
        Sale.objects.create(
            product=self.product,
            customer=self.customer2,
            date=date.today(),
            quantity=5
        )
        response = self.client.get(
            reverse('sales'), {'ordering': 'total_sales', 'group_by': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['total_sales'], '500.00')
        self.assertEqual(response.data['results'][1]['total_sales'], '1100.00')
