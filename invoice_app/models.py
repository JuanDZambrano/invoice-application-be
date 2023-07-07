from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import (CATEGORY_CHOICES, CUSTOMER, PAYMENT_METHOD_CHOICES,
                        PROVIDER, STATUS_CHOICES)


class Product(models.Model):
    name = models.CharField(
        max_length=255, help_text="The name of the product."
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The price of the product."
    )

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter the name of the contact."
    )
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        help_text="Select the category of the contact."
    )

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product",
        help_text="Select the product for the sale."
    )
    customer = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        limit_choices_to={'category': CUSTOMER},
        verbose_name="Customer",
        help_text="Select the customer for the sale."
    )
    date = models.DateField(
        verbose_name="Date",
        help_text="Enter the date of the sale."
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity",
        help_text="Enter the quantity sold."
    )

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "sale"
        verbose_name_plural = "sales"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["product"], name="sale_product_idx"),
        ]

    def __str__(self):
        return f"Sale #{self.pk}"


class Debt(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product",
        help_text="Select the product associated with the debt."
    )
    provider = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        limit_choices_to={'category': PROVIDER},
        verbose_name="Provider",
        help_text="Select the provider associated with the debt."
    )
    date = models.DateField(
        verbose_name="Date",
        help_text="Enter the date of the debt."
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Enter the amount of the debt."
    )
    due_date = models.DateField(
        verbose_name="Due Date",
        help_text="Enter the due date of the debt."
    )

    class Meta:
        verbose_name = "debt"
        verbose_name_plural = "debts"
        ordering = ["-due_date"]
        indexes = [
            models.Index(fields=["product"], name="debt_product_idx"),
        ]

    def __str__(self):
        return f"Debt #{self.pk}"


class Employee(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="Enter the name of the employee."
    )
    date_hired = models.DateField(
        verbose_name="Date Hired",
        help_text="Enter the date when the employee was hired."
    )
    date_terminated = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date Terminated",
        help_text="Enter the date when the employee was terminated, if applicable."
    )
    wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Wage",
        help_text="Enter the wage/salary of the employee."
    )

    @property
    def salary(self):
        # Assuming a monthly salary
        end_date = self.date_terminated if self.date_terminated else datetime.now().date()
        months_worked = (end_date - self.date_hired).days // 30
        return self.wage * months_worked

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"
        ordering = ["name"]

    def __str__(self):
        return self.name


class EmployeeExpense(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Employee",
        help_text="Select the employee associated with the expense."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Enter the amount of the expense."
    )
    date = models.DateField(
        verbose_name="Date",
        help_text="Enter the date of the expense."
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Description",
        help_text="Enter a description of the expense."
    )

    class Meta:
        verbose_name = "employee expense"
        verbose_name_plural = "employee expenses"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["employee"],
                         name="employee_expense_employee_idx"),
        ]

    def __str__(self):
        return f"Expense #{self.pk}"


class Invoice(models.Model):

    transaction_date = models.DateField(
        verbose_name=_("Transaction Date"),
        help_text=_("Enter the date of the transaction.")
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name=_("Contact"),
        help_text=_("Select the contact associated with the transaction.")
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
        help_text=_("Select the employee associated with the transaction.")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name=_("Payment Method"),
        help_text=_("Select the payment method for the transaction.")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("Status"),
        help_text=_("Select the status of the invoice.")
    )
    transaction_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Transaction Number"),
        help_text=_("Unique transaction number."),
        blank=True
    )
    sales = models.ManyToManyField(
        Sale,
        verbose_name=_("Sales"),
        help_text=_("Select the sales associated with the invoice.")
    )

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"Invoice #{self.transaction_number}"

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            date_str = datetime.now().strftime('%Y%m%d')
            unique_id = str(self.pk) if self.pk else str(
                Invoice.objects.latest('id').id + 1)
            self.transaction_number = f'INV-{date_str}-{unique_id}'
        super().save(*args, **kwargs)
