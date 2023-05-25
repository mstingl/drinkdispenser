from django.contrib import admin
from .models import Card, Drink, DrinkIngredient, Ingredient


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


class DrinkIngredientInline(admin.StackedInline):
    model = DrinkIngredient


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    inlines = [DrinkIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
