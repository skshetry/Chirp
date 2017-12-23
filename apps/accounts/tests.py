"""Tests for accounts app."""
from django.test import TestCase
from django.shortcuts import reverse
from accounts.forms import UserAuthenticationForm
# Create your tests here.


class LoginTest(TestCase):
    """This tests the login view."""

    def setUp(self):
        """Set things up for testing login functionality."""
        self.url = reverse('accounts:login')
        self.response = self.client.get(self.url)

    def test_csrf(self):
        """Test for csrf token."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests if it contains form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserAuthenticationForm)

    def test_response_status_code(self):
        """Tests for `OK` response."""
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_is_rendered(self):
        """Tests if `accounts/login.html` and `base.html` is used."""
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertTemplateUsed(self.response, 'base.html')
