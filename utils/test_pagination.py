from django.test import TestCase
# from django.core.paginator import Paginator
# from recipes.models import Recipe
from utils.pagination import make_pagination_range
from django.urls import reverse


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self): # noqa E501
        # Current page = 1 - Qty pages = 4 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        # Current page = 2 - Qty pages = 4 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        # Current page = 18 - Qty pages = 4 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        # Current page = 19 - Qty pages = 4 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        # Current page = 20 - Qty pages = 4 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_first_page_if_current_page_is_bigger_than_middle_page(self):
        # Current page = 3 - Qty pages = 4 - Middle page = 2
        pagination_first_page_out_of_range = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )['first_page_out_of_range']
        self.assertTrue(pagination_first_page_out_of_range)
        # Current page = 4 - Qty pages = 4 - Middle page = 2
        pagination_first_page_out_of_range = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )['first_page_out_of_range']
        self.assertTrue(pagination_first_page_out_of_range)

    def test_last_page_if_current_page_is_less_than_total_pages_minus_middle_page(self): # noqa E501
        # Current page = 17 - Qty pages = 4 - Middle page = 2
        pagination_last_page_out_of_range = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=17
        )['last_page_out_of_range']
        self.assertTrue(pagination_last_page_out_of_range)
        # Current page = 16 - Qty pages = 4 - Middle page = 2
        pagination_last_page_out_of_range = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=16
        )['last_page_out_of_range']
        self.assertTrue(pagination_last_page_out_of_range)

    def test_search_return_correct_template(self):
        response = self.client.get(
            reverse('recipes:search') + '?q=teste'
        )
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
