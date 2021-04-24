from rest_framework.permissions import BasePermission


class IsCreatorUser(BasePermission):
    """
    Allows access only to creator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'myuser') and request.user.myuser.is_creator)


class IsStudentUser(BasePermission):
    """
    Allows access only to student users.
    """

    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'myuser') and request.user.myuser.is_student)


class IsCreatorOrAdminUser(BasePermission):
    """
    Allows access only to creator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff) or bool(request.user and hasattr(request.user, 'myuser') and request.user.myuser.is_creator)
