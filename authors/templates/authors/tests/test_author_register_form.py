from authors.forms import RegisterForm
from django.test import TestCase

class AuthorRegisterFormUnitTest(TestCase):
    def test_first_name_placeholder(self):
        form = RegisterForm()
        placeholder = form.fields['first_name'].widget.attrs['placeholder']
        self.assertEqual(placeholder, 'Ex.: John')