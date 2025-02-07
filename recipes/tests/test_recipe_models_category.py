from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(
            category_name='Category Test'
        )
        
        return super().setUp()
    
    def test_recipe_category_model_string_representation(self):
        self.assertEqual(
            str(self.category), self.category.name
        )
    def test_receipe_category_title_raises_error_if_title_has_more_than_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()  
        