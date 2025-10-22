# habits/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать только свои записи. Публичные привычки доступны для чтения всем.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.is_public:
                return True
            return obj.owner == request.user
        return obj.owner == request.user
