from djoser.serializers import SetPasswordSerializer, UserCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from recipes.models import Recipe
from users.models import CustomUser, Subscribe


class IsSubscribed(metaclass=serializers.SerializerMetaclass):
    """Метакласс для отображения факта подписки"""

    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Subscribe.objects.filter(
                user=request.user, author_id=obj.id).exists():
            return True
        return False


class UserRecordSerializer(UserCreateSerializer, IsSubscribed):
    """Сериализатор на запись для пользователей"""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_subscribed')

    def validate_username(self, value):
        """Проверка имени пользователя"""

        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Имя {value} не может быть использовано'
            )
        return value

    def to_representation(self, obj):
        """Отдаем данные пользователя без пароля"""

        data = super(UserRecordSerializer, self).to_representation(obj)
        data.pop('password', None)
        return data


class CustomUserReadSerializer(ModelSerializer, IsSubscribed):
    """Сериализатор на чтение для пользователей"""

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed'
        )


class UserSetPasswordSerializer(SetPasswordSerializer):

    class Meta:
        model = CustomUser
        fields = ('new_password', 'current_password')


class RecipeShortSerializer(ModelSerializer):
    """Усеченный сериализатор для Рецептов"""

    model = Recipe
    fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(ModelSerializer, IsSubscribed):
    """Сериализатор для Подписок"""

    recipes = SerializerMethodField()
    recipe_numbers = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipe_numbers')

    def get_recipe_numbers(self, obj):
        author = get_object_or_404(CustomUser, id=obj.id)
        return author.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        author = get_object_or_404(CustomUser, id=obj.id)
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = author.recipes[:recipes_limit]
        else:
            queryset = author.recipes
        return RecipeShortSerializer(queryset, many=True).data
