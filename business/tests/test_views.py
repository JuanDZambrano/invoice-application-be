from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts.models import CustomUser
from business.models import Company, Order, OrderItem, Product


class OrderItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        self.user = CustomUser.objects.create_user(
            username='john',
            email='john@email.com',
            password='testpass123',
            company=self.company,
            user_type='BM'
        )
        self.superuser = CustomUser.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123',
            user_type='AD'
        )
        self.order = Order.objects.create(
            company=self.company,
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            status='DR'
        )
        self.product = Product.objects.create(
            name='Test Product',
            company=self.company,
            description='',
            unit_price=10.0
        )
        self.order_item = OrderItem.objects.create(
            amount=5,
            price=10.0,
            order=self.order,
            product=self.product,
            company=self.company
        )
        # Login the user to set the JWT token in an HTTP-only cookie
        self.client = APIClient()
        data = {'email': 'john@email.com', 'password': 'testpass123'}
        login_response = self.client.post(reverse('rest_login'), data)
        assert 'app-auth' in self.client.cookies  # Ensure the JWT cookie is set
        assert login_response.status_code == 200

    def test_update_orderitem(self):
        data = {"amount": 20, "price": 30.0}
        response = self.client.patch(
            reverse('orderitem-detail', kwargs={'pk': self.order_item.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_data(self):
        data = {"amount": "invalid", "price": "invalid"}
        response = self.client.post(reverse('orderitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_other_users_company(self):
        other_company = Company.objects.create(
            name="Other Company",
            address="456 Other St",
            phone="0987654321",
            email="othercompany@email.com",
            tax_id="987654321",
        )
        other_order = Order.objects.create(
            company=other_company,
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            status='DR'
        )
        other_order_item = OrderItem.objects.create(
            amount=5,
            price=10.0,
            order=other_order,
            product=self.product,
            company=other_company
        )
        response = self.client.get(
            reverse('orderitem-detail', kwargs={'pk': other_order_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get(
            reverse('orderitem-detail', kwargs={'pk': self.order_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_by_order(self):
        response = self.client.get(
            reverse('orderitem-list'), {'group_by': 'order'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_orderitem(self):
        response = self.client.delete(
            reverse('orderitem-detail', kwargs={'pk': self.order_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_orderitem(self):
        response = self.client.get(
            reverse('orderitem-detail', kwargs={'pk': self.order_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_orderitem(self):
        data = {
            "amount": 10,
            "price": 20.0,
            "order": self.order.id,
            "product": self.product.id,
            "company": self.company.id
        }
        response = self.client.post(reverse('orderitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orderitems(self):
        response = self.client.get(reverse('orderitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
