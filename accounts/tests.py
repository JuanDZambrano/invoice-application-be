from django.contrib.auth import get_user_model
from django.test import TestCase

from .constants import USER_TYPE_CHOICES
from .models import Company


class CustomUserTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='john',
            email='john@email.com',
            password='testpass123',
            company=self.company,
            user_type=USER_TYPE_CHOICES[1][0]
        )
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@email.com')
        self.assertEqual(user.company, self.company)
        self.assertEqual(user.user_type, USER_TYPE_CHOICES[1][0])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123',
            company=self.company,
            user_type=USER_TYPE_CHOICES[0][0]
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertEqual(admin_user.company, self.company)
        self.assertEqual(admin_user.user_type, USER_TYPE_CHOICES[0][0])
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.username = 'newuser'
        self.email = 'newuser@email.com'

    def test_signup(self):
        User = get_user_model()
        new_user = User.objects.create_user(
            username='john',
            email='john@email.com',
            password='testpass123',
            company=self.company,
            user_type=USER_TYPE_CHOICES[0][0]
        )
        self.assertEqual(
            User.objects.all().count(), 1
        )
        self.assertEqual(
            User.objects.all()
            [0].username, new_user.username
        )
        self.assertEqual(
            User.objects.all()
            [0].email, new_user.email
        )
