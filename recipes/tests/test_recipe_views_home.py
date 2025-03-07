from django.urls import reverse, resolve
from recipes import views
# Create your tests here.
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:home'))
        # content = response.content.decode('utf-8')
        response_content_recipes = response.context['recipes']
        # self.assertIn(recipe.title, content)
        self.assertEqual(len(response_content_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is not published"""
        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:home'))
        response_content_recipes = response.context['recipes']
        self.assertEqual(len(response_content_recipes), 0)


    def test_recipe_home_view_returns_200_OK(self):
        response = self.client.get(
            reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):

        response = self.client.get(
            reverse('recipes:home'))
        self.assertIn(b'<h1>No recipes found here</h1>', response.content)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch()
        response = self.client.get(
            reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 4)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
    # tres recetas por página

    @patch('recipes.views.PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):
        for i in range(12):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)
        response = self.client.get(
            reverse('recipes:home') + '?page=1A'
            )
        ...
        self.assertEqual(
            response.context['recipes'].number, 1
            )
        response = self.client.get(
            reverse('recipes:home') + '?page=2'
            )
        ...
        self.assertEqual(
            response.context['recipes'].number, 2
            )
