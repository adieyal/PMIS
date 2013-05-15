from django.views.generic import DetailView
from project.apps.projects.decorators import group_required
from project.apps.projects.mixins import GroupRequiredMixin
from project.apps.projects.models import Project


class ProjectView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        print self.object.programme.client.name
        group_required(self.object.programme.client.name)
        return super(ProjectView, self).get_context_data(**kwargs)












