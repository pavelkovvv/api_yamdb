from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Пользовательское разрешение, позволяющее выполнять
    действия только администратору или если это безопасный метод"""

    def has_permission(self, request, view):
        return (
                request.user.is_admin or
                request.user.is_staff or
                request.method in permissions.SAFE_METHODS
        )


class AuthorOrModerOrAdmin(permissions.BasePermission):
    """Пользовательское разрешение, позволяющее выполнять действия,
    если ваша роль соответствует следующим: автор, модератор или Вы
    являетесь автором объекта"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_moderator or
            request.user.is_admin or
            request.user.is_staff or
            obj.author == request.user
        )


class OnlyAdmin(permissions.BasePermission):
    """Пользовательское разрешение, позволяющее выполнять действия
    только администратору"""

    def has_permission(self, request, view):
        return (
                request.user.is_staff
                or (
                    request.user.is_authenticated
                    and request.user.is_admin
                )
        )
