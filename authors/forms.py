import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing}{attr_new_val}'


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    """
    Validates that a password is strong by ensuring it contains at least one 
    uppercase letter, one lowercase letter, one number, and is at least 
    8 characters long.

    Args:
        password (str): The password to validate.

    Raises:
        ValidationError: If the password does not meet the criteria.
    """

    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Type your password again')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        error_messages={
            'required': 'El usuario es requerido',
            'unique': 'El usuario ya existe',
            'invalid': 'El usuario es invalido',
            'min_length': 'Asegúrese de que este valor tenga al menos 4 carácter(es)',
            'max_length': 'Asegúrese de que este valor tenga menos de 150 carácter(es)',
        },
        help_text='Obligatorio. El nombre de usuario debe  tener menos de 150 caracteres' 
                  'y contener solo letras, números y @/./+/-/_.',
        required=True,
        label='Usuario',
        min_length=4,
        max_length=150,
    )
    first_name = forms.CharField(
        error_messages={
            'required': 'El nombre es requerido'
        },
        help_text='Nombre',
        required=True,
        label='Nombre'
    )
    last_name = forms.CharField(
        error_messages={
            'required': 'El apellido es requerido'
        },
        help_text='Apellido',
        required=True,
        label='Apellido'
    )
    email = forms.EmailField(
        error_messages={
            'required': 'El correo es requerido'
        },
        help_text='Correo electronico',
        required=True,
        label='Correo'
    )
     
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'La contraseña no debe estar en blanco'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Contraseña'
    )
    password2 = forms.CharField(
        error_messages={
            'required': 'Por favor repita la contraseña'
        },
        required=True,
        widget=forms.PasswordInput(),
        label='Contraseña2'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        # labels = {
        #     'username': 'Usuario',
        # }
        # labels = {
        #     'first_name': 'Nombre',
        #     'last_name': 'Apellido',
        #     'email': 'Correo',
        #     'password': 'Contraseña',
        #     'username': 'Usuario'
        # }
        
        # help_texts = {
        #     'email': 'Correo electronico',
        #     'first_name': 'Nombre',
        #     'last_name': 'Apellido'
        # }
        # help_texts = {
        #     'username': 'Obligatorio. El nombre de usuario debe  tener menos de 150 caracteres' 
        #                 'y contener solo letras, números y @/./+/-/_.',
        # },
        # error_messages = {
        #     'username': {
        #         'required': 'El usuario es requerido',
        #         'unique': 'El usuario ya existe',
        #         'invalid': 'El usuario es invalido',
        #     }
        # }

        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={'placeholder': 'Ej: Juan', 'class': 'input text-input'}
        #         ),
        #     'password': forms.PasswordInput(
        #         attrs={'placeholder': 'Ej: 12345678'}
        #         ),
        # }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atencion' in data:
            raise ValidationError(
                'No se permite la palabra %(cosa)s en el campo de password',
                code='invalid',
                params={'cosa': 'atencion'})
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if 'Juan Perez' in data:
            raise ValidationError(
                'No se permite la palabra %(value)s en el campo de first_name',
                code='invalid',
                params={'value': 'Juan Perez'})
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exist = User.objects.filter(email=email).exists()
        if exist:
            raise ValidationError(
                f'El correo {email} ya existe',
                code='invalid'
            )
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            password_confirmation_error = ValidationError(
                'Los passwords no son iguales',
                code='invalid'  
            )    
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [password_confirmation_error,
                              'Los passwords no son iguales jiji']
            })