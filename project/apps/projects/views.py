from braces.views import LoginRequiredMixin
from django.views.generic import DetailView
from project.apps.projects.models import Project
from project.apps.projects.utils import group_required


class ProjectView(LoginRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        group_required(self.request, self.object.programme.client.name, self.object.municipality.all()[0].district.name)
        return super(ProjectView, self).get_context_data(**kwargs)












