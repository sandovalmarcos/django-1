from django.views import View
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
        login_required(login_url='authors:login', redirect_field_name='next',
                       ),
        name='dispatch',
    )
class DashboardRecipe(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,  # só receitas do usuário logado
                pk=id,
            ).first()

            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html',
                      context={
                          'form': form,
                          })

    def get(self, request, id=None):
        print('que pasa?')
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.is_published = False
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.save()
            messages.success(request, 'Recipe updated successfully')
            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(recipe.id,)))
        return self.render_recipe(form)


class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Deleted successfully')
        return redirect(reverse('authors:dashboard'))
