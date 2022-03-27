from datetime import datetime, timedelta
from django.test import TestCase

from .models import Food, Weight, Recipe
from .views import dish_calories_per100g
import unittest
unittest.TestLoader.sortTestMethodsUsing = None


class TestDishCaloriesPer100G(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for data in (1, 'Food1', 10), (2, 'Food2', 30), (3, 'Food3', 50):
            Food(*data).save()

        Recipe(
            1, 'Recipe1', 'Text', 'other', 'recipe1', timedelta(minutes=5), datetime.now()
        ).save()

        Recipe(
            2, 'Recipe2', 'Text', 'other', 'recipe2', timedelta(minutes=5), datetime.now()
        ).save()
        for data in (1, 1, 1, 100), (2, 1, 2, 400), (3, 1, 3, 300):
            Weight(*data).save()

    def test_simple_recipe_average_calorie(self):
        self.assertEqual(dish_calories_per100g('recipe1'), 35)

    def test_empty_recipe_returns_hyphen(self):
        self.assertEqual(dish_calories_per100g('recipe2'), '-')
