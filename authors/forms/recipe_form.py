from django import forms
from recipes.models import Recipe
from utils.django_form import add_attr
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError


class AuthorRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_attr(self.fields['preparation_steps'], 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned = self.cleaned_data

        title = cleaned.get('title')
        description = cleaned.get('description')
        if title == description:
            self._my_errors['title'].append('Title and description must be different') # noqa E501
            self._my_errors['description'].append('Title and description must be different') # noqa E501
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self._my_errors['title'].append('Title must have at least 5 characters') # noqa E501
        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        if is_positive_number(field_value) is False:
            self._my_errors[field_name].append('Must be a positive number')
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        if is_positive_number(field_value) is False:
            self._my_errors[field_name].append('Must be a positive number')
        return field_value
