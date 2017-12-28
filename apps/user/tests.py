"""Tests for the Change Password view."""

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase


class PasswordChangeTests(TestCase):
    """Class for the change password tests."""

    def setUp(self):
        """Contains the functions for the tests."""
        username = 'john'
        password = 'secret123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        url = reverse('user:change_password')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        """Tests if the page exists i.e. a 200 status check."""
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        """Tests if the url is correct for changing password."""
        view = resolve('/user/settings/change-password/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def test_csrf(self):
        """Checking if the csrf token is sent."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests if the response page contains the password changing forms."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        """
        Tests if the page contains all the fields i.e. 3 password fields and the csrf token.
        """
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
    """Tests if user can access the pw change page without loggin in."""

    def test_redirection(self):
        """Test for redirection after unauthorized access."""
        url = reverse('user:change_password')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    """
    Base test case for form processing
    accepts a `data` dict to POST to the view.
    """
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('user:change_password')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            })

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        # FIXME: Is this really the way to go?
        self.assertEqual(self.url + 'done/', reverse('user:password_change_done'))

    def test_password_changed(self):
        """
        refresh the user instance from database to get the new password
        hash updated by the change password view.
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        """
        response = self.client.get(reverse('Home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        """
        refresh the user instance from the database to make
        sure we have the latest data.
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
