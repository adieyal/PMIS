from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from project.apps.projects.decorators import group_required


class GroupRequiredMixin(object):
    group_list = []
    print object

    @method_decorator(login_required)
    @method_decorator(group_required(group_list))
    def dispatch(self, *args, **kwargs):
        return super(GroupRequiredMixin, self).dispatch(*args, **kwargs)