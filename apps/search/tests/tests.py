'''
Tests for search app
'''
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase


# Create your tests here.
class searchTest(TestCase):
    '''
    Includes seach test as much as possible
    '''

    def setUp(self):
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@mail.com",
            password="pass_word"
        )
        self.other_user = get_user_model().objects.create_user(
            username="other_user",
            email="other@mail.com",
            password="pass_word"
        )
        self.client.login(username='test_user', password='pass_word')
        self.other_client.login(
            username='other_user', password='pass_word')

    def test_response_status_code(self):
        """Tests for `OK` response."""
        self.url = reverse('search:search')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)

# class searchLink(searchTest):
#     '''
#     Includes the test for search redirection
#     '''
#     def setUp(self):
#         self.url = reverse('search:search')
#         self.response = self.client.get(self.url)

#     def test_response_status_code(self):
#         """Tests for `OK` response."""
#         self.assertEqual(self.response.status_code, 200)
