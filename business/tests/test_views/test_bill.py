from datetime import datetime

from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import CustomUser
from business.models import Bill, Company


class BillViewSetTestCase(APITestCase):
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
        self.bill = Bill.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            amount=100.0,
            type='TP',
            company=self.company,
            status='PE'
        )
        # Login the user to set the JWT token in an HTTP-only cookie
        self.client = APIClient()
        data = {'email': 'john@email.com', 'password': 'testpass123'}
        login_response = self.client.post(reverse('rest_login'), data)
        assert 'app-auth' in self.client.cookies  # Ensure the JWT cookie is set
        assert login_response.status_code == 200

    def test_list_bills(self):
        response = self.client.get(reverse('bill-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_bill(self):
        data = {
            "due_date": "2023-12-31T00:00:00Z",
            "amount": 200.0,
            "type": "TP",
            "company": self.company.id,
            "status": "PE"
        }
        response = self.client.post(reverse('bill-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_bill(self):
        data = {"amount": 150.0, "status": "CO"}
        response = self.client.patch(
            reverse('bill-detail', kwargs={'pk': self.bill.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_bill(self):
        response = self.client.delete(
            reverse('bill-detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_bill(self):
        response = self.client.get(
            reverse('bill-detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        client = APIClient()
        response = client.get(
            reverse('bill-detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_total_bill_value_in_date_range_and_status(self):
        # Create additional Bills for testing
        Bill.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            amount=50.0,
            type='TP',
            company=self.company,
            status='PE'
        )
        Bill.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            amount=20.0,
            type='TP',
            company=self.company,
            status='PE'
        )

        str_gte = '01-01-23'
        str_lte = '01-01-24'
        bill_status = 'PE'
        bill_type = 'TP'

        url = reverse('bill-total-bill-value-in-date-range-and-status')
        response = self.client.get(
            url, {'date__gte': str_gte, 'date__lte': str_lte, 'status': bill_status, 'type': bill_type})

        expected_total_value = Bill.objects.filter(
            due_date__gte=timezone.make_aware(
                datetime.strptime(str_gte, '%d-%m-%y')),
            due_date__lte=timezone.make_aware(
                datetime.strptime(str_lte, '%d-%m-%y')),
            status=bill_status
        ).aggregate(Sum('amount'))['amount__sum']

        self.assertEqual(response.data['total_value'], expected_total_value)
