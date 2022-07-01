from http import HTTPStatus

from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from users.models import CustomUser, Subscribe
from .serializers import (CustomUserReadSerializer, UserRecordSerializer,
                          UserSetPasswordSerializer, SubscribeSerializer)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для обработки запросов к пользователям"""

    serializer_class = UserRecordSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return UserSetPasswordSerializer
        if self.action == 'me':
            return CustomUserReadSerializer
        return UserRecordSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к подпискам"""

    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(CustomUser, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(CustomUser, id=author_id)
        Subscribe.objects.create(user=request.user, author=author)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe,
            user__id=user_id,
            author__id=author_id
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)
