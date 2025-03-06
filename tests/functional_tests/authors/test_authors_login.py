import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorBaseFunctionalTest
@pytest.mark.functional_test
class AuthorLoginTest(AuthorBaseFunctionalTest):
    
    def test_user_valid_data_can_login_successfully(self):
        psw = 'my_password'
        user = User.objects.create_user(username='my_user', password=psw)
        
        # El usuario abre la página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        # El usuario ve el formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        
        # El usuario digita su nombre de usuario y contraseña
        username_field.send_keys(user.username)
        password_field.send_keys(psw)
        
        # El usuario envia el formulario
        form.submit()
        self.assertIn(
            f'You are logged in with {user.username}. Please Click here to logout',
            self.browser.find_element(By.TAG_NAME, 'body').text
                      )
        
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
    
    def test_login_form_is_invalid(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
    def test_login_form_invalid_credentials(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        form.submit()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
    
        