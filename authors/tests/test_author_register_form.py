from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Type your password again'),
    ])
    def test_fields_placeholder(self, field, placeholder_value):
        form = RegisterForm()
        placeholder = form.fields[field].widget.attrs['placeholder']
        self.assertEqual(placeholder, placeholder_value)
        
    @parameterized.expand([
        ('username', 'Obligatorio. El nombre de usuario debe  tener menos de 150 caracteres' 
                     'y contener solo letras, números y @/./+/-/_.'),
        ('password', 'Password must have at least one uppercase letter, '
                     'one lowercase letter and one number. The length should be '
                     'at least 8 characters.'),
        ('email', 'El correo debe tener el formato: usuario@dominio.com.'),
        ('first_name', 'Escriba su nombre'),
        ('last_name', 'Escriba su apellido'),
    ])
    def test_fields_help_text(self, field, needed_value):
        form = RegisterForm()
        placeholder = form[field].help_text
        self.assertEqual(placeholder, needed_value)
    @parameterized.expand([
        ('username', 'Usuario'),
        ('first_name', 'Nombre'),
        ('last_name', 'Apellido'),
        ('email', 'Correo'),
        ('password', 'Contraseña'),
        ('password2', 'Contraseña2'),
    ])
    def test_fields_label(self, field, needed_value):
        form = RegisterForm()
        placeholder = form[field].label
        self.assertEqual(placeholder, needed_value)
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.form_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'yMm0G@example.com',
            'password': 'T3stP@ssw0rd',
            'password2': 'T3stP@ssw0rd',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'El usuario es requerido'),
        ('first_name', 'El nombre es requerido'),
        ('last_name', 'El apellido es requerido'),
        ('email', 'El correo es requerido'),
        ('password', 'La contraseña no debe estar en blanco'),
        ('password2', 'Por favor repita la contraseña'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    def test_username_field_min_lenght_should_be_4(self):
        self.form_data['username'] = 'tes'
        url = reverse('authors:register_create')
        msg = 'Asegúrese de que este valor tenga al menos 4 carácter(es)'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('username'))
    def test_username_field_max_lenght_should_be_150(self):
        self.form_data['username'] = 'A'*151
        url = reverse('authors:register_create')
        msg = 'Asegúrese de que este valor tenga menos de 150 carácter(es)'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_password_field_have_lower_upper_number(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)  
        msg = ('Password must have at least one uppercase letter, '
        'one lowercase letter and one number. The length should be '
        'at least 8 characters.')
             
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))
        
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)  
        msg = ('Los passwords no son iguales')
             
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)  
        self.assertNotIn(msg, response.content.decode('utf-8'))
        
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_email_field_is_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = f'El correo ya existe'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )
        self.assertTrue(is_authenticated)