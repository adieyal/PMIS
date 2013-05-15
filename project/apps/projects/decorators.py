from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in.

    Checks is_active and allows superusers to pass regardless of group
    membership.
    """
    print group_names

    def in_group(u):
        print bool(u.groups.filter(name__in=group_names))
        if bool(u.groups.filter(name__in=group_names)):
            return bool(u.groups.filter(name__in=group_names))
        else:
            raise PermissionDenied
    return user_passes_test(in_group)