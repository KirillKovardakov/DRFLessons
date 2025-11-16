from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    message = 'Adding customer not allowed.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """
    message = 'You are not an Owner.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
