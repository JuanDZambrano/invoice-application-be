from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def __init__(self, company_model: None) -> None:
        self.company_model = company_model
        super().__init__()

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not email:
            raise ValueError('The Email field must be set')

        # Create a default company for superusers
        company, created = self.company_model.objects.get_or_create(
            name='Default Company')
        extra_fields['company'] = company

        return self.create_user(username, email, password, **extra_fields)
