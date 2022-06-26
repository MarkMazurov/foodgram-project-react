import webcolors

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import (SerializerMethodField, CharField,
                                        CurrentUserDefault, SlugRelatedField,
                                        PrimaryKeyRelatedField, IntegerField,
                                        UniqueTogetherValidator)

from recipes.models import (Ingredient, Favorite, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.serializers import CustomUserReadSerializer


class HexColor(serializers.Field):
    """Кастомный тип поля для обработки цвета"""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Нет имени для цвета!')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    color = HexColor()

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение для связанной таблицы рецептов и ингредиентов"""

    id = IntegerField(source='ingredient.id', read_only=True)
    name = CharField(source='ingredient.name', read_only=True)
    measurement_unit = CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientRecordSerializer(serializers.ModelSerializer):
    """Сериализатор на запись для связанной таблицы рецептов и ингредиентов"""

    id = IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение для рецептов"""

    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientReadSerializer(
        read_only=True,
        many=True,
        source='recipeingredients'
    )
    author = CustomUserReadSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ['pub_date']

    def get_is_favorited(self, obj):
        """Добавлен ли рецепт с Избранное"""

        request = self.context.get('request')
        return (request.user.is_authenticated and Favorite.objects.filter(
            user=request.user, recipe__id=obj.id).exists())

    def get_is_in_shopping_cart(self, obj):
        """Добавлен ли рецепт в Список покупок"""

        request = self.context.get('request')
        return (request.user.is_authenticated and ShoppingCart.objects.filter(
            user=request.user, recipe__id=obj.id).exists())


class RecipeRecordSerializer(serializers.ModelSerializer):
    """Сериализатор на запись/удаление для рецептов"""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientRecordSerializer(
        many=True,
        source='recipeingredients'
    )
    image = Base64ImageField(max_length=None, use_url=False)

    class Meta:
        model = Recipe
        exclude = ['pub_date']
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name'),
                message='Вы уже добавили рецепт с таким названием!'
            )
        ]

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        if validated_data.get('tags'):
            instance.tags.set(validated_data.get('tags', instance.tags))
        instance.ingredients.clear()
        for ingredient in validated_data['recipeingredients']:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=instance,
                amount=ingredient['amount']
            )
        validated_data.pop('recipeingredients')
        super().update(instance, validated_data)
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранного"""

    id = IntegerField(read_only=True, source='recipe.id')
    name = CharField(read_only=True, source='recipe.name')
    image = Base64ImageField(
        max_length=None,
        use_url=False,
        read_only=True,
        source='recipe.image'
    )
    cooking_time = IntegerField(read_only=True, source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка Покупок"""

    id = IntegerField(read_only=True, source='recipe.id')
    name = CharField(read_only=True, source='recipe.name')
    image = Base64ImageField(
        max_length=None,
        use_url=False,
        read_only=True,
        source='recipe.image'
    )
    cooking_time = IntegerField(read_only=True, source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
