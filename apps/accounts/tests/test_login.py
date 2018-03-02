"""Tests for accounts app."""
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from accounts.forms import CustomUserAuthenticationForm, SignUpForm

# Create your tests here.


class LoginGETTest(TestCase):
    """Tests the login view `GET`."""

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
        self.assertIsInstance(form, CustomUserAuthenticationForm)

    def test_response_status_code(self):
        """Tests for `OK` response."""
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_is_rendered(self):
        """Tests if `accounts/login.html` and `base.html` is used."""
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_contains_signup_link(self):
        """Test if it contains `signup` link."""
        url = reverse('accounts:signup')
        self.assertContains(self.response, 'href="' + url + '"')

    def test_contains_forgot_password_link(self):
        """Test if it contains `forgot_password` link."""
        # DONE: Changed this to test for actual link
        url = reverse('accounts:password_reset')
        self.assertContains(self.response, url)

    def test_form_inputs(self):
        """The view must contain three inputs: csrf, username, password."""
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 1)


class LoginPostTest(TestCase):
    """Tests the login `POST` requests."""

    def setUp(self):
        """Set ups the user and url for this test."""
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user('foo', 'mail@example.com', 'bar')

    def test_empty_password_post_data(self):
        """Test empty password `POST`."""
        data = {
            'username': self.user.username,
            'password': '',  # Empty password
        }

        response = self.client.post(self.url, data)

        # Assert that the form has error on `password` field.
        error_message = ['This field is required.']
        self.assertFormError(response, 'form', 'password', error_message)

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Test that the template is same.
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the redirect does not occur.
        # Redirect shouldn't occur after invalid login.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)

    def test_wrong_user_password_post_data(self):
        """Test wrong password :login:."""
        data = {
            'username': self.user.username,
            'password': 'foobar',  # Wrong password data
        }
        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect does not occur.
        # Redirect occurs after successful login.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)

        # Assert that the form has error.
        error_message = 'Please enter a correct username and password. ' 'Note that both fields may be case-sensitive.'
        self.assertFormError(response, 'form', None, error_message)

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_successfull_post_login_data(self):
        """
        Test successful :login:.

        Also, test for default redirection to `LOGIN_REDIRECT_URL`.
        """
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur.
        # Redirect occurs after successful login.
        self.assertRedirects(response, expected_url=reverse(
            settings.LOGIN_REDIRECT_URL
        ), status_code=302
        )

        # Test that the template is not used. Because, it must be a redirection.
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')

        # Test that the user is logged in.
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_successfull_post_login_redirects_next(self):
        """
        Test successful :login:.

        Also, test for redirection, specified in `next`.
        """
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(
            self.url + '?next=' + reverse('feeds:home'), data)

        # Test that the redirect doesnot occur.
        # Redirect occurs after successful login.
        self.assertRedirects(
            response,
            expected_url=reverse('feeds:home'),
            status_code=302
        )

        # Test that the template isnot used. Because, it must be a redirection.
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')

        # Test that the user is logged in.
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_empty_username_post_data(self):
        """Test for empty username post."""
        data = {
            'username': '',
            'password': 'bababa',  # Empty password
        }
        response = self.client.post(self.url, data)

        # Assert that the form has error.
        error_message = ['This field is required.']
        self.assertFormError(response, 'form', 'username', error_message)

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the redirect doesnot occur.
        # Redirect occurs after successful login.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)

    def test_wrong_username_post_data(self):
        """Test for wrong user details."""
        data = {
            'username': 'fppnar',  # Wrong username
            'password': 'foobar',  # Wrong password data
        }
        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur.
        # Redirect occurs after successful login.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)

        # Assert that the form has error.
        error_message = 'Please enter a correct username and password. ' 'Note that both fields may be case-sensitive.'
        self.assertFormError(response, 'form', None, error_message)

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())


class UnverifiedEmailUsersLoginTest(TestCase):
    """Tests for user with unverified email."""

    def setUp(self):
        """Make the user inactive."""
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user(
            'foo',
            'mail@example.com',
            'bar',
            is_active=False
        )

    def test_post_login(self):
        """Test login failure."""
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur.
        # Redirect occurs after successful login.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)

        error_message = "The email has not been verified. Please check your email\
        for verification link."
        self.assertFormError(response, 'form', None, error_message)

        # Test that the template isnot used.
        # Because, it must not be a redirection.
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())


class LogoutTest(TestCase):
    """Test for logging users out."""

    def setUp(self):
        """Set the user, log it in and go to `logout` link`."""
        self.user = User.objects.create_user(
            'hansolo',
            'hansolo@millienium.falcon',
            'princessleia'
        )
        self.url = reverse('accounts:logout')
        self.client.login(
            username=self.user.username,
            password=self.user.password
        )
        self.response = self.client.get(self.url)

    def test_logout_user_is_deauthenticated(self):
        """Tests for deauthentication."""
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_logout_redirects_to_login_page(self):
        """Test for redirection to login page."""
        self.assertRedirects(
            self.response,
            expected_url=reverse('accounts:login'),
            status_code=302
        )


class SignupGetTest(TestCase):
    """Tests the signup view `GET`."""

    def setUp(self):
        """Set things up for testing signup functionality."""
        self.url = reverse('accounts:signup')
        self.response = self.client.get(self.url)

    def test_csrf(self):
        """Test for csrf token."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests if it contains form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_response_status_code(self):
        """Tests for `OK` response."""
        self.assertEqual(self.response.status_code, 200)

    def test_signup_view_is_rendered(self):
        """Tests if `accounts/signup.html` and `base.html` is used."""
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
        self.assertTemplateUsed(self.response, 'base.html')

        # unable to link, need assistance

    def test_contains_login_link(self):
        """Test if it contains `signup` link."""
        url = reverse('accounts:login')
        self.assertContains(self.response, f'href="{url}"')

    def test_form_inputs(self):
        """The view must contain three inputs: csrf, username, first_name, last_name
        email, password1, password2"""
        self.assertContains(self.response, '<input', 7)
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="password"', 2)


class SignupPostTest(TestCase):
    """Tests the login `POST` requests."""

    def setUp(self):
        """Set ups the user and url for this test."""
        self.url = reverse('accounts:signup')

    def test_successfull_post_signup(self):
        data = {
            'username': 'testusername',
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'email': 'testemail@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',

        }

        response = self.client.post(self.url, data)

        user = User.objects.get(username=data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertFalse(user.is_active)
        self.assertTrue(user)

        self.assertTemplateUsed(response, 'accounts/email_sent.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertEqual(response.status_code, 200)

    def test_password_mismatch(self):
        data = {
            'username': 'testusername1',
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'email': 'testemail@gmail.com',
            'password1': 'testpassword1',
            'password2': 'testpassword2',
        }

        response = self.client.post(reverse('accounts:signup'), data)

        error_messages = ["The two password fields didn't match."]
        self.assertFormError(response, 'form', 'password2', error_messages)
        self.assertFalse(User.objects.filter(
            username=data['username']).exists())

        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertEqual(response.status_code, 200)
