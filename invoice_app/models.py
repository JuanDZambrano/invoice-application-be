from django.db import models
from datetime import datetime
from .constants import (CATEGORY_CHOICES,
                        CUSTOMER,
                        PROVIDER)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE, limit_choices_to={
        'category': CUSTOMER})
    date = models.DateField()
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Debt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Contact, on_delete=models.CASCADE, limit_choices_to={
                                 'category': PROVIDER})
    date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField()


class Employee(models.Model):
    name = models.CharField(max_length=255)
    date_hired = models.DateField()
    date_terminated = models.DateField(null=True, blank=True)
    wage = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def salary(self):
        # Assuming a monthly salary
        end_date = self.date_terminated if self.date_terminated else datetime.now().date()
        months_worked = (end_date - self.date_hired).days // 30
        return self.wage * months_worked


class EmployeeExpense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
