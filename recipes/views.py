# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from utils.recipes.factory import make_recipe
from utils.pagination import make_pagination
from recipes.models import Recipe
import os
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
# from django.contrib import messages
from django.forms.models  import model_to_dict

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'
    paginate_by = None

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE)
        ctx.update({
                'recipes': page_obj,
                'pagination_range': pagination_range,
                }
        )
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
        })
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            {
                'recipes': list(recipes_list)
             },
        )

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(

            category__id=self.kwargs.get('category_id')
        )
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'title': f'{ctx.get("recipes")[0].category.name} - Category',
            }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        if not search_term:
            raise Http404()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
              )
        )
        print(qs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        ctx.update(
            {
                'page_title': f'Search for "{search_term}" |',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}',
            }
        )
        return ctx

class RecipeDetailAPI(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''


        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']
        return JsonResponse(
            recipe_dict,
            safe=False,
        )
