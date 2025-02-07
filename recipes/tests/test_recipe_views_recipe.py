from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views

class RecipeViewsRecipeTest(RecipeTestBase):
    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', args=[1]))
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_recipe_view_returns_200_OK(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:recipe', args=[1])
        )
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_recipe_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_recipe_template_loads_correct_recipe(self):
        needed_title = 'Recipe Test'
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': 1
                    }
                )
            )
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_recipe_template_dont_load_recipes_not_published(self):
        """
        Test recipe is not published
        """
        recipe =self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe.id
                    }
                )
            )
        
        self.assertEqual(response.status_code, 404)