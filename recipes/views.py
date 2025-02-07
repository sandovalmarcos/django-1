# Create your views here.
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from utils.recipes.factory import make_recipe
from utils.recipes.pagination import make_pagination
from recipes.models import Recipe
import os
# from django.contrib import messages

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
        ).order_by('-id')

    # messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    # messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        }
                  )


def category(request, category_id):
    """
    This view will render the recipes by category.
    :param category_id: The category id to filter the recipes
    :return: A rendered template with the recipes from the category
    """
    # recipes = Recipe.objects.filter(
    #     category__id=category_id,
    #     is_published=True,
    # ).order_by('-id')
    # if not recipes:
    #     raise Http404('No hay mano')
    # category_name = getattr(
    #     getattr(recipes.first(), 'category', None), 'name', 'Not found')
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'title': f'{recipes[0].category.name} | Category',
        'pagination_range': pagination_range,
    })


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            pk=id,
            is_published=True,
        )
    )
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404('Not found')
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term)
        & Q(is_published=True)
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/search.html',
                  context={
                      'recipes': page_obj,
                      'search_term': search_term,
                      'pagination_range': pagination_range,
                      'aditional_querystring': f'&q={search_term}'
                  })
