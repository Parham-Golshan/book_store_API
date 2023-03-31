from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Returns True if the user is the owner of the object, else False.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author.user == request.user
