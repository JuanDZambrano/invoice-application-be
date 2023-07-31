import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager

from .constants import USER_TYPE_CHOICES


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tax_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Company: {self.name}>"


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)

    objects = CustomUserManager(company_model=Company)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<CustomUser: {self.username}>"
