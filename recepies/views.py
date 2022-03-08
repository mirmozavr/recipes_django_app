from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import F, Q
from .models import Food, Recepies, Weight


def index(request):
    return HttpResponse('My text')


def recepies(request):
    qs = Recepies.objects.order_by('-modified').all()
    return render(request, 'recepies/recepies.html', {'qs': qs})


def single_recepie(request, slug: str):
    rec = get_object_or_404(Recepies, slug=slug)
    qs = get_list_or_404(Weight, recepie=rec)
    return render(request, 'recepies/single_recepie.html', {'rec': rec, 'qs': qs})
