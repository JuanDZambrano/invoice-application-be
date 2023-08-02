from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from accounts.models import Company

from .constants import (BILL_STATUS_CHOICES, BILL_TYPE_CHOICES,
                        ORDER_STATUS_CHOICES)
from .models import (Bill, Category, Customer, Employee, Job, Location, Order,
                     OrderItem, Payment, Product)


class CompanyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(str(self.company), "Test Company")


class EmployeeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.job = Job.objects.create(
            name="Test Job",
            remuneration=1000.00,
            company=cls.company,
        )
        cls.employee = Employee.objects.create(
            name="Test Employee",
            company=cls.company,
            email="testemployee@email.com",
            job=cls.job,
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Test Employee")
        self.assertEqual(str(self.employee), "Test Employee")


class LocationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(
            name="Test Location",
            address="123 Test St",
        )

    def test_location_creation(self):
        self.assertEqual(self.location.name, "Test Location")
        self.assertEqual(str(self.location), "Test Location")


class JobTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.job = Job.objects.create(
            name="Test Job",
            remuneration=1000.00,
            company=cls.company,
        )

    def test_job_creation(self):
        self.assertEqual(self.job.name, "Test Job")
        self.assertEqual(str(self.job), "Test Job")


class CustomerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.customer = Customer.objects.create(
            name="Test Customer",
            phone="1234567890",
            email="testcustomer@email.com",
            notes="Test Notes",
            company=cls.company,
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(str(self.customer), "Test Customer")


class CategoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            company=cls.company,
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(str(self.category), "Test Category")


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            company=cls.company,
        )
        cls.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            unit_price=10.00,
            inventory=100,
            category=cls.category,
            company=cls.company,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(str(self.product), "Test Product")


class PaymentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.payment = Payment.objects.create(
            name="Test Payment",
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.name, "Test Payment")
        self.assertEqual(str(self.payment), "Test Payment")


class OrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.customer = Customer.objects.create(
            name="Test Customer",
            phone="1234567890",
            email="testcustomer@email.com",
            notes="Test Notes",
            company=cls.company,
        )
        cls.payment = Payment.objects.create(
            name="Test Payment",
        )
        cls.order = Order.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            customer=cls.customer,
            payment_method=cls.payment,
            company=cls.company,
            status=ORDER_STATUS_CHOICES[0][0],
        )

    def test_order_creation(self):
        self.assertEqual(str(self.order), f"Order {self.order.id}")


class OrderItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            company=cls.company,
        )
        cls.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            unit_price=10.00,
            inventory=100,
            category=cls.category,
            company=cls.company,
        )
        cls.customer = Customer.objects.create(
            name="Test Customer",
            phone="1234567890",
            email="testcustomer@email.com",
            notes="Test Notes",
            company=cls.company,
        )
        cls.payment = Payment.objects.create(
            name="Test Payment",
        )
        cls.order = Order.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            customer=cls.customer,
            payment_method=cls.payment,
            company=cls.company,
            status=ORDER_STATUS_CHOICES[0][0],
        )
        cls.order_item = OrderItem.objects.create(
            amount=1,
            price=10.00,
            order=cls.order,
            product=cls.product,
            company=cls.company,
        )

    def test_order_item_creation(self):
        self.assertEqual(str(self.order_item),
                         f"Order Item {self.order_item.id}")


class BillTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            address="123 Test St",
            phone="1234567890",
            email="testcompany@email.com",
            tax_id="123456789",
        )
        cls.bill = Bill.objects.create(
            due_date=timezone.make_aware(datetime(2023, 12, 31)),
            amount=100.00,
            type=BILL_TYPE_CHOICES[0][0],
            company=cls.company,
            status=BILL_STATUS_CHOICES[0][0],
        )

    def test_bill_creation(self):
        self.assertEqual(
            str(self.bill), f"{self.bill.type} - {self.bill.amount}")
