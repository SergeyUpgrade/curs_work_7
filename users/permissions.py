from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """Проверка, принадлежит ли объект пользователю, с котором осуществляется действие."""

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False
