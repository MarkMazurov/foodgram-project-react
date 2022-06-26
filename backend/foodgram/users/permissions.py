from rest_framework.permissions import BasePermission, SAFE_METHODS


class CurrentUserOrAdminOnly(BasePermission):
    """
    Кастомный пермишен: доступ только для
    текущего пользователя, либо администратора
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or request.user.is_admin


class ReadOnly(BasePermission):
    """Кастомный пермишен: доступ только на чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """Кастомный пермишен: доступ для автора, либо на чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
