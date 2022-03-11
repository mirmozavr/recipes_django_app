from django.db import connection
from django.db.models import Sum, Avg, Value, Count, Max, Min
from django.shortcuts import render, get_object_or_404
from .models import Recepies


def recepies(request):
    qs = Recepies.objects.order_by('-modified').all()
    return render(request, 'recepies/recepies.html', {'qs': qs})


def single_recepie(request, slug: str):
    recipe = get_object_or_404(Recepies, slug=slug)
    qs = recipe.weight_set.all()
    dc = dish_calorage_per100g(slug)
    return render(request, 'recepies/single_recepie.html', {'rec': recipe, 'qs': qs, 'dc': dc})


def dish_calorage_per100g(slug):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT SUM(rf.calorie * rw.weight)/SUM(rw.weight)
        FROM recepies_recepies rr JOIN recepies_weight rw ON (rr.id = rw.recepie_id)
        JOIN recepies_food rf ON (rw.food_id = rf.id)
        WHERE rr.slug = %s
        """, [slug])

        calorage = cursor.fetchone()
        return calorage[0] or 0

