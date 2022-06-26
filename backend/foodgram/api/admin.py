from django.contrib.admin import ModelAdmin, site, TabularInline

from recipes.models import (Ingredient, Favorite, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import CustomUser, Subscribe


class UserAdmin(ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'date_joined')
    list_display_links = ('pk', 'username', 'email')
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


class TagAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'


class IngredientAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_display_links = ('pk', 'name',)
    search_fields = ('name',)
    list_editable = ('measurement_unit',)
    empty_value_display = '-пусто-'


class IngredientInline(TabularInline):
    model = Ingredient
    fields = ('name', 'measurement_unit')


class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_display_links = ('recipe', 'ingredient')
    inlines = [
        IngredientInline
    ]


class RecipeIngredientInline(TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


class RecipeAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'text', 'cooking_time',
                    'pub_date', 'add_to_favorites')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)
    inlines = [
        RecipeIngredientInline,
    ]
    autocomplete_fields = ('author', 'tags')
    list_filter = ('author', 'tags')
    empty_value_display = '-пусто-'

    def add_to_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class FavoriteAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_display_links = ('pk', 'user')


class ShoppingCartAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_display_links = ('pk', 'user')


class SubscribeAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_display_links = ('pk', 'user')
    search_fields = ('user', 'author')


site.register(CustomUser, UserAdmin)
site.register(Tag, TagAdmin)
site.register(Ingredient, IngredientAdmin)
site.register(Recipe, RecipeAdmin)
site.register(Favorite, FavoriteAdmin)
site.register(ShoppingCart, ShoppingCartAdmin)
site.register(Subscribe, SubscribeAdmin)


site.site_header = 'Проект Foodgram'
