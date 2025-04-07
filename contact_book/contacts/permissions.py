from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.role not in roles:
                raise PermissionDenied("You don't have permission to access this page.")

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


class RoleRequiredMixin(UserPassesTestMixin):
    roles_required = []

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role in self.roles_required
        )


class SuperAdminRequiredMixin(RoleRequiredMixin):
    roles_required = ["SUPER_ADMIN"]


class AdminRequiredMixin(RoleRequiredMixin):
    roles_required = ["SUPER_ADMIN", "ADMIN"]


class OwnershipRequiredMixin:
    """
    Mixin to ensure users can only modify their own objects
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)
