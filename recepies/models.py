from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Recepies(models.Model):
    FOOD_TYPE_CHOICE = [
        ('meat', 'Meat'),
        ('vegan', 'Vegan'),
        ('bakery', 'Bakery'),
        ('fish', 'Fish'),
        ('salad', 'Salad'),
        ('soup', 'Soup'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=128, unique=True, null=False)
    text = models.CharField(max_length=500)
    branch = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICE, default='other')
    slug = models.SlugField(default='', unique=True, blank=True)
    food = models.ManyToManyField('Food', null=True, blank=True, through='Weight')
    cooking_time = models.DurationField(default=timedelta(), null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Food(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    calorie = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Weight(models.Model):
    recepie = models.ForeignKey(Recepies, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    weight = models.IntegerField(default=0)

    def __repr__(self):
        return f"{self.food} - {self.weight}gr for {self.recepie}"

    def __str__(self):
        return self.__repr__()
