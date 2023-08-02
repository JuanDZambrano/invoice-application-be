import uuid

from django.db import models

from accounts.models import Company

from .constants import (BILL_STATUS_CHOICES, BILL_TYPE_CHOICES,
                        ORDER_STATUS_CHOICES)


class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    remuneration = models.FloatField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Job: {self.name}>"

    class Meta:
        verbose_name_plural = "Jobs"


class Employee(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='employees')
    email = models.EmailField()
    job = models.ForeignKey(
        Job, null=True, on_delete=models.SET_NULL, related_name='jobs')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Employee: {self.name}>"

    class Meta:
        verbose_name_plural = "Employees"


class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Location: {self.name}>"

    class Meta:
        verbose_name_plural = "Locations"


class Customer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Customer: {self.name}>"

    class Meta:
        verbose_name_plural = "Customers"


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: {self.name}>"

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_price = models.FloatField()
    inventory = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Product: {self.name}>"

    class Meta:
        verbose_name_plural = "Products"


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Payment: {self.name}>"

    class Meta:
        verbose_name_plural = "Payments"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    payment_method = models.ForeignKey(
        Payment, null=True, on_delete=models.PROTECT, related_name='orders')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES)
    employee = models.ForeignKey(
        Employee, null=True, on_delete=models.SET_NULL, related_name='orders')
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')

    def __str__(self):
        return f"Order {self.id}"

    def __repr__(self):
        return f"<Order: {self.id}>"

    class Meta:
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    amount = models.IntegerField()
    price = models.FloatField()
    total_price = models.FloatField(default=0.0, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name='order_items')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='order_items')

    def __str__(self):
        return f"Order Item {self.id}"

    def __repr__(self):
        return f"<OrderItem: {self.id}>"

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Order Items"


class Bill(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    due_date = models.DateTimeField()
    amount = models.FloatField()
    type = models.CharField(max_length=2, choices=BILL_TYPE_CHOICES)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='bills')
    status = models.CharField(max_length=2, choices=BILL_STATUS_CHOICES)

    def __str__(self):
        return f"{self.type} - {self.amount}"

    def __repr__(self):
        return f"<Bill: {self.type} - {self.amount}>"

    class Meta:
        verbose_name_plural = "Bills"
