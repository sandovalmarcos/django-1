from django.core.exceptions import ValidationError
import re


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
