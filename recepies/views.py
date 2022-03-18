from django.db import connection
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from .models import Recipe


def display_all_recipes(request):
    """
    Display all recepies.Recepies model objects
    """
    qs = Recipe.objects.order_by('-modified').all()

    search_form = SearchForm()
    return render(request, 'recepies/recepies.html', {'qs': qs, 'search_form': search_form})


def recipe_search(request):
    """
    Display search results.
    """
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        word = search_form.cleaned_data['word']
        title_search_qs = Recipe.objects.filter(title__icontains=word).order_by('-modified').all()
        ingredient_search_qs = Recipe.objects.filter(Q(food__name__icontains=word), ~Q(title__icontains=word))
        ingredient_search_qs.query.group_by = ['id']
    else:
        title_search_qs, ingredient_search_qs = None, None
    search_form = SearchForm()
    print(title_search_qs, ingredient_search_qs)
    return render(request, 'recepies/search.html', {'ts': title_search_qs,
                                                    'ings': ingredient_search_qs,
                                                    'search_form': search_form})


def display_single_recipe(request, slug: str):
    """
    Display an individual recepies.Recipe model object,
    all connected recepies.Weight and recepies.Food objects
    and average dish colorage.
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    qs = recipe.weight_set.all()
    dc = dish_calories_per100g(slug)
    return render(request, 'recepies/single_recepie.html', {'rec': recipe, 'qs': qs, 'dc': dc})


def dish_calories_per100g(slug: str):
    """
    Calculate average dish calories for recepies.Recipe object
    via designated slug. Implemented by raw sql queries.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT SUM(rf.calorie * rw.weight)/SUM(rw.weight)
        FROM recepies_recipe rr JOIN recepies_weight rw ON (rr.id = rw.recipe_id)
        JOIN recepies_food rf ON (rw.food_id = rf.id)
        WHERE rr.slug = %s
        """, [slug])

        calories = cursor.fetchone()
        return calories[0] or 0
