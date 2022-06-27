import textwrap

from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный слаг',
        unique=True
    )
    color = models.CharField(
        max_length=20,
        verbose_name='Цветовой HEX-код',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return textwrap.shorten(self.name, width=30)


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return textwrap.shorten(self.name, width=30)


class Recipe(models.Model):
    """Модель рецепта"""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        db_index=True
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    image = models.ImageField(
       verbose_name='Картинка',
       upload_to='image/recipes/'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=1,
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_recipes'
            )
        ]

    def __str__(self) -> str:
        return textwrap.shorten(self.name, width=30)


class RecipeIngredient(models.Model):
    """Связанная модель рецептов и ингредиентов"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self) -> str:
        return "{}_{}".format(
            self.recipe.__str__(), self.ingredient.__str__())


class Favorite(models.Model):
    """Модель избранных рецептов"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorites'
            )
        ]

    def __str__(self) -> str:
        return "{}_{}".format(self.user, self.recipe)


class ShoppingCart(models.Model):
    """Модель списка покупок"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_carts'
            )
        ]

    def __str__(self) -> str:
        return "{}_{}".format(self.user, self.recipe)
