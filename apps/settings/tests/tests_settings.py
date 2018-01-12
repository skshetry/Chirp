"""Tests for the Settings view."""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class LoggedInUserSettingsViewTest(TestCase):
    def setUp(self):
        username = 'john'
        password = 'secret123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        url = reverse('settings:settings')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_templates(self):
        self.assertTemplateUsed(self.response, 'settings.html')
        self.assertTemplateUsed(self.response, 'base.html')
    
    def test_has_change_password_link(self):
        change_password_link = reverse('settings:change_password')
        self.assertContains(self.response, f'href="{change_password_link}"')


class LoggedOutUserSettingsTestCase(TestCase):
    def setUp(self):
        self.url = reverse('settings:settings')
        self.response = self.client.get(self.url)

    def test_redirects(self):
        redirect_url = reverse('accounts:login')
        self.assertRedirects(
            self.response,
            expected_url=f'{redirect_url}?next={self.url}',
            status_code=302
        )
