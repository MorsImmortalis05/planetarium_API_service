from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUpdateCreateOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        elif request.method in ("POST", "PUT"):
            return request.user and request.user.is_staff
        return False


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user == obj.user or request.user.is_staff
