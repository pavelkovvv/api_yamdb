from rest_framework import permissions


class IsAuthPermission(permissions.BasePermission):
    """Пользовательское разрешение, позволяющее выполнять
    действия только авторизованному пользователю"""

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Пользовательское разрешение, позволяющее выполнять
    действия только администратору или если это безопасный метод"""

    def has_permission(self, request, view):
        return (
                request.user.is_admin or
                (request.user.is_authenticated and
                 request.method in permissions.SAFE_METHODS)
                )


class IsAdminUser(permissions.BasePermission):
    """Разрешение только для администраторов."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


# !!!!!ДОПИСАТЬ РАЗРЕШЕНИЯ И ПЕРЕЙТИ К СОЗДАНИЮ ЕНДПОИНТА USERS (вьюсеты для него и т.п., пример в предыдущем спринте)