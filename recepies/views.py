from django.db import connection
from django.db.models import Sum, Avg, Value, Count, Max, Min, Q
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from .models import Recipe


def display_all_recipes(request):
    """
    Display all recepies.Recepies model objects
    """
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            qs = Recipe.objects.filter(Q(title__icontains=search_form.cleaned_data['word'])).order_by('-modified').all()

    else:
        qs = Recipe.objects.order_by('-modified').all()

    search_form = SearchForm()
    return render(request, 'recepies/recepies.html', {'qs': qs, 'search_form': search_form})


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

        calorage = cursor.fetchone()
        return calorage[0] or 0
