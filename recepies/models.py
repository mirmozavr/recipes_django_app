from datetime import datetime, timedelta

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
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, unique=True, null=False)
    text = models.CharField(max_length=500)
    branch = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICE, default='other')
    slug = models.SlugField(default='', blank=True)
    food = models.ManyToManyField('Food', null=True, blank=True)
    cooking_time = models.DurationField(default=timedelta(), null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.modified = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Food(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=False)
    calorie = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


