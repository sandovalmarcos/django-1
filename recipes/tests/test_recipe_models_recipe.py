from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
                    category=self.make_category(category_name='Test Default Category'),
                    author=self.make_author(username='newuser'),
                    title = 'Test Recetas 2',
                    description = 'Descipción recetas 2',
                    slug = 'test 2',
                    preparation_time = '200',
                    preparation_time_unit = 'minutos',
                    servings = '20',
                    servings_unit = 'porciones',
                    preparation_steps = 'Recipe steps 2',
                )
        self.recipe.full_clean()
        self.recipe.save()
        return recipe
    
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 66
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, type_field, max_length):
        
        setattr(self.recipe, type_field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
                         'preparation_steps_is_html must be false by default'
                         )
        
    def test_recipe_is_published_is_false_by_default(self):
        
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
                         'is_published must be false by default'
                         )
        
    def test_recipe_string_representation(self):
        self.recipe.title = 'Recipe Test'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual('Recipe Test', str(self.recipe))
        
        