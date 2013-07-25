from django.core.exceptions import PermissionDenied


def group_required(request, *group_names):
    if request.user.groups.filter(name__in=group_names).count() == len(group_names):
        return request.user.groups.filter(name__in=group_names).count() == len(group_names)
    else:
        raise PermissionDenied
