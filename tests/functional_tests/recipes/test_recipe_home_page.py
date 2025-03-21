from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest
from unittest.mock import patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuario abre la página
        self.browser.get(self.live_server_url)

        # Encuentra el campo de búsqueda y realiza la búsqueda
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Buscar recetas..."]'
        )
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # Espera a que el elemento .main-content-list esté
        main_content = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'main-content-list')
                )
        )

        # Verifica que el título buscado esté en el contenido
        self.assertIn(
            title_needed,
            main_content.text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_is_paginated(self):
        self.make_recipe_in_batch()
        # Usuario abre la pagina
        self.browser.get(self.live_server_url)

        # Mira que hay una paginación y clickea en la segunda pagina
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Ve que la segunda pagina tiene el contenido correcto
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2  # 2 es el numero de recetas por pagina
        )
