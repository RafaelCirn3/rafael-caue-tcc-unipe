from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrGlobalReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'usuario', None)

        if owner is None:
            return request.method in SAFE_METHODS

        return owner == request.user
