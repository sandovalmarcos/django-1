from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeMixin:
    def make_category(self, category_name='Category'):
        return Category.objects.create(name=category_name)

    def make_author(self,
                    first_name='User',
                    last_name='Test',
                    username='user',
                    password='123456',
                    email='K6E0U@example.com',
                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            )

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Test Recetas',
                    description='Descipción recetas',
                    slug='test',
                    preparation_time='20',
                    preparation_time_unit='minutos',
                    servings='20',
                    servings_unit='porciones',
                    preparation_steps='Recipe steps',
                    preparation_steps_is_html=False,
                    is_published=True,
                    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
    
    def make_recipe_in_batch(self, qty=10):
        recipes = []
        for i in range(qty):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()

    