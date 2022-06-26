from http import HTTPStatus

from django.http import FileResponse
from django.db.models import Exists, OuterRef, Sum
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .utils import pdf_file_create
from recipes.models import (Ingredient, Favorite, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.permissions import AuthorOrReadOnly, ReadOnly
from .filters import IngredientFilter, RecipeFilter
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeRecordSerializer, TagSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к тегам"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к ингредиентам"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (ReadOnly,)
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к рецептам"""

    serializer_class = RecipeRecordSerializer
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Recipe.objects.all()
        queryset = Recipe.objects.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                user=self.request.user, recipe_id=OuterRef('pk')
            )),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                user=self.request.user, recipe_id=OuterRef('pk')
            ))
        )
        if self.request.GET.get('is_favorited'):
            return queryset.filter(is_favorited=True)
        if self.request.GET.get('is_in_shopping_cart'):
            return queryset.filter(is_in_shopping_cart=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeRecordSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к списку избранных рецептов"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    pagination_class = None

    def favorite_create(self, request, *args, **kwargs):
        """Кастомный метод для добавления рецепта в избранное"""

        pk = int(self.kwargs['recipe_id'])
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data, HTTPStatus.CREATED)

    def favorite_delete(self, request, *args, **kwargs):
        """Кастомный метод для удаления рецепта из избранного"""

        pk = int(self.kwargs['recipe_id'])
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=recipe
        )
        favorite.delete()
        return Response(HTTPStatus.NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к списку покупок"""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    pagination_class = None

    def cart_create(self, request, *args, **kwargs):
        """Кастомный метод для добавления рецепта в список покупок"""

        pk = int(self.kwargs['recipe_id'])
        recipe = get_object_or_404(Recipe, id=pk)
        cart = ShoppingCart.objects.create(user=request.user, recipe=recipe)
        serializer = ShoppingCartSerializer(cart, context={'request': request})
        return Response(serializer.data, HTTPStatus.CREATED)

    def cart_delete(self, request, *args, **kwargs):
        """Кастомный метод для удаления рецепта из списка покупок"""

        pk = int(self.kwargs['recipe_id'])
        recipe = get_object_or_404(Recipe, id=pk)
        cart = get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe
        )
        cart.delete()
        return Response(HTTPStatus.NO_CONTENT)


class ShoppingCartDownloadViewSet(viewsets.ModelViewSet):
    """Вьюсет для загрузки списка покупок"""

    def download(self, request):
        """Кастомный метод для создания и скачивания списка покупок"""

        shopping_cart = RecipeIngredient.objects.filter(
            recipe__shopping_carts__user=request.user).values(
                'ingredient__name', 'ingredient__measurement_unit').order_by(
                    'ingredient__name').annotate(
                        ingredient_total=Sum('amount'))
        downloading_file = pdf_file_create(shopping_cart, 'Список покупок')
        return FileResponse(
            downloading_file,
            as_attachment=True,
            filename='shopping_cart.pdf',
            status=HTTPStatus.OK
        )
