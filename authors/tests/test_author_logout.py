from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        # Arrange
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')
        response = self.client.get(
            reverse('authors:logout'), 
            follow=True)
        
        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )
        
    def test_user_tries_to_logout_as_another_user(self):
        # Arrange
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')
        response = self.client.post(
            reverse('authors:logout'), 
            follow=True, 
            data={'username': 'my_other_user'}
            )
        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )
    
    def test_user_logout_successfully(self):
        # Arrange
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')
        response = self.client.post(
            reverse('authors:logout'), 
            follow=True,
            data={'username': 'my_user'}
            )
        self.assertIn(
            'Logged out successfully',
            response.content.decode('utf-8')
        )
        