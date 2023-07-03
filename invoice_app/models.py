from django.db import models
from .constants import CATEGORY_CHOICES


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE, limit_choices_to={
                                 'category': Contact.CUSTOMER})
    date = models.DateField()
    quantity = models.PositiveIntegerField()


class Debt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Contact, on_delete=models.CASCADE, limit_choices_to={
                                 'category': Contact.PROVIDER})
    date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField()


class Employee(models.Model):
    name = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
