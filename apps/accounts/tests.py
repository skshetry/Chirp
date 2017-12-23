"""Tests for accounts app."""
from django.test import TestCase
from django.shortcuts import reverse
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
