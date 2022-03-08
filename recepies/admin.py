from django.contrib import admin
from .models import Recepies, Food, Weight
# Register your models here.


class WeightInline(admin.TabularInline):
    model = Weight
    extra = 1


@admin.register(Recepies)
class RecepiesAdmin(admin.ModelAdmin):
    list_display = ('_id', 'title', 'text', 'cooking_time', 'slug', 'branch', 'modified')
    list_editable = ('title', 'text', 'branch', 'cooking_time')
    ordering = ('-modified',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('food',)
    inlines = (WeightInline,)


class CalorieFilter(admin.SimpleListFilter):
    title = 'calorie filter'
    parameter_name = 'calorie'

    def lookups(self, request, model_admin):
        return [
            ('0-100', '0-100'),
            ('101-200', '101-200'),
            ('201-300', '201-300'),
            ('301-500', '301-500'),
            ('501-700', '501-700'),
            ('>700', '>700'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-100':
            return queryset.filter(calorie__lte=100)
        if self.value() == '101-200':
            return queryset.filter(calorie__gte=101, calorie__lte=200)
        if self.value() == '201-300':
            return queryset.filter(calorie__gte=201, calorie__lte=300)
        if self.value() == '301-500':
            return queryset.filter(calorie__gte=301, calorie__lte=500)
        if self.value() == '501-700':
            return queryset.filter(calorie__gte=501, calorie__lte=700)
        if self.value() == '>700':
            return queryset.filter(calorie__gte=700)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('_id', 'name', 'calorie', 'nutrition')
    list_editable = ('name', 'calorie')
    ordering = ('name', '-calorie')
    list_per_page = 100
    search_fields = ('name', 'calorie')
    list_filter = [CalorieFilter]

    @admin.display(ordering='calorie', description='Nutritive')
    def nutrition(self, food: Food):
        if food.calorie <= 100:
            return 'Very low'
        if food.calorie <= 200:
            return 'Low'
        if food.calorie <= 300:
            return 'Good'
        if food.calorie <= 500:
            return 'High'
        if food.calorie <= 700:
            return 'Very high'
        return 'Unhealthy'