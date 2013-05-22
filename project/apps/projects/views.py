from braces.views import LoginRequiredMixin
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import DetailView
from project.apps.projects.models import Project


class ProjectView(LoginRequiredMixin, DetailView):
    model = Project

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        try:
            queryset = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise Http404
        try:
            queryset = Project.objects.get_project(self.request.user.id).get(id=pk)
        except Project.DoesNotExist:
            raise PermissionDenied

        return queryset


class CreateProjectWizard(SessionWizardView):
    template_name = 'formtools/wizard/wizard_form.html'











