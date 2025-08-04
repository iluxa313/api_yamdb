from rest_framework import permissions

ROLES = ['admin', 'moderator']


class AdminPermissionForUsers(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'admin'


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.role == 'admin'
        )


class UserOrModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PATCH']:
            return (request.user.is_superuser or request.user.role in ROLES
                    or request.user == obj.author)
        else:
            return request.user.is_authenticated
