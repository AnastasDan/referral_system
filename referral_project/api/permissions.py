from rest_framework import permissions


class OwnerOnlyPermission(permissions.BasePermission):
    """
    Пользовательское разрешение.
    Разрешает чтение или изменение/удаление объекта только самому пользователю.
    """

    def has_object_permission(self, request, view, obj):
        """
        Определяет право доступа пользователя к объекту.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.id == request.user.id
        )
