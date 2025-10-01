from django.test import TestCase, Client
from django.urls import reverse
from .models import Account

class AccountModelTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            is_active=True
        )

    def test_account_str(self):
        self.assertEqual(str(self.account), 'testuser')

class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            is_active=True
        )

    # Add view tests here as needed, e.g. registration, login, etc.
    # Example:
    # def test_login_view(self):
    #     response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
    #     self.assertEqual(response.status_code, 200)
