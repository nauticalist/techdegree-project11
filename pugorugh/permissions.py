from rest_framework import permissions


class UpdateOwnPreferences(permissions.BasePermission):
    """
    Allow users to edit their own preferences
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own preferences
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.pk


class UpdateOwnDog(permissions.BasePermission):
    """
    Allow users to edit and delete their own dogs
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user.id == request.user.pk