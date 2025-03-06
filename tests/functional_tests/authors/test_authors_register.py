
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import AuthorBaseFunctionalTest

@pytest.mark.functional_test
class AuthorRegisterTest(AuthorBaseFunctionalTest):    
    
    
    def fill_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*10)
                
    def get_form(self, form=2):
        return self.browser.find_element(
            By.XPATH,
            f'/html/body/main/div[{form}]/form'
        )
        
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('email@gmail.com')
        callback(form)
        return form
    
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name = self.get_by_placeholder(form, 'Ex.: John')
            first_name.send_keys(' ')
            first_name.send_keys(Keys.ENTER)
            form = self.get_form(3)
            self.assertIn(
                'El nombre es requerido',
                form.text
            )
        self.form_field_test_with_callback(callback)
    
    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name.send_keys(' ')
            last_name.send_keys(Keys.ENTER)
            form = self.get_form(3)
            self.assertIn(
                'El apellido es requerido',
                form.text
            )
        self.form_field_test_with_callback(callback)
        
    def test_empty_username_error_message(self):
        def callback(form):
            username = self.get_by_placeholder(form, 'Your username')
            username.send_keys(' ')
            username.send_keys(Keys.ENTER)
            form = self.get_form(3)
            self.assertIn(
                'El usuario es requerido',
                form.text
            )
        self.form_field_test_with_callback(callback)
        
    def test_invalid_email_error_message(self):
        def callback(form):
            email = self.get_by_placeholder(form, 'Your e-mail')
            email.send_keys('correo@correo')
            email.send_keys(Keys.ENTER)
            self.sleep()
            form = self.get_form()
            self.assertIn(
                'El correo debe tener el formato: usuario@dominio.com.',
                form.text
            )
        self.form_field_test_with_callback(callback)
        
    def test_password_mismatch(self):
        def callback(form):
            pasword1 = self.get_by_placeholder(form, 'Type your password')
            pasword2 = self.get_by_placeholder(form, 'Type your password again')
            pasword1.send_keys('password')
            pasword2.send_keys('P@ssw0rd2')
            pasword2.send_keys(Keys.ENTER)
            form = self.get_form(3)
            
            self.assertIn(
                'Los passwords no son iguales',
                form.text
            )
        self.form_field_test_with_callback(callback)
    
    def test_user_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.get_by_placeholder(form, 'Your username').send_keys('my_user')
        self.get_by_placeholder(form, 'Ex.: John').send_keys('John')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Doe')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@gmail.com')
        self.get_by_placeholder(form, 'Type your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(form, 'Type your password again').send_keys('P@ssw0rd1')
        form.submit()
        self.assertIn(
            'User created successfully. Please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )