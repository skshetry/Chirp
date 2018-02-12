"""Tests for Status code Errors."""

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.shortcuts import render_to_response
from .views import server_error, not_found, permission_denied, bad_request


class ErrorViewTestCase(object):
    """Main class for Errors."""

    ERROR_CODE = None
    ERROR_BASE_TEMPLATE = 'error_base.html'
    ERROR_TEMPLATE_VIEW = None
    HOMEPAGE_LINK = reverse('feeds:home')
    factory = RequestFactory()
    views = {500: server_error, 400: bad_request,
             403: permission_denied, 404: not_found}

    def setUp(self):
        """Create request and response for the errors."""
        self.request = self.factory.get('/')
        self.response = self.views[self.ERROR_CODE](self.request)

    def test_status_code(self):
        """Tests for checking the status code."""
        self.assertEqual(self.response.status_code, self.ERROR_CODE)

    def assertTemplateUsed(self, response, template_name):
        """Check if the correct template is used for errors."""
        self.assertEqual(self.response.content,
                         render_to_response(template_name).content)

    def test_are_templates_rendered(self):
        """Tests for checking if the correct template is loaded."""
        self.assertTemplateUsed(self.response, self.ERROR_TEMPLATE_VIEW)

    def test_contains_homepage_link(self):
        """Checks if there is HomePage link in the rendered error template."""
        self.assertTrue(self.HOMEPAGE_LINK in str(self.response.content))


class HTTPNotFoundTest(ErrorViewTestCase, TestCase):
    """Testing for 404 Errors."""

    ERROR_CODE = 404
    ERROR_TEMPLATE_VIEW = str(ERROR_CODE) + '.html'


class HTTPServerErrorTest(ErrorViewTestCase, TestCase):
    """Testing for 500 Errors."""

    ERROR_CODE = 500
    ERROR_TEMPLATE_VIEW = str(ERROR_CODE) + '.html'


class HTTPBadRequestTest(ErrorViewTestCase, TestCase):
    """Testing for 400 Errors."""

    ERROR_CODE = 400
    ERROR_TEMPLATE_VIEW = str(ERROR_CODE) + '.html'


class HTTPPermissonDeniedTest(ErrorViewTestCase, TestCase):
    """Testing for 403 Errors."""

    ERROR_CODE = 403
    ERROR_TEMPLATE_VIEW = str(ERROR_CODE) + '.html'
