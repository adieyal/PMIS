from braces.views import LoginRequiredMixin
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import DetailView, ListView
from project.apps.projects.forms import ProjectForm, LocationAndScopeFormContainer, ProjectRoleFormSet
from project.apps.projects.models import Project


FORMS = [('project_form', ProjectForm),
         ('location_and_scope_form', LocationAndScopeFormContainer),
         ('project_role_form', ProjectRoleFormSet), ]

TEMPLATES = {'project_form': 'formtools/wizard/project_form.html',
             'location_and_scope_form': 'formtools/wizard/location_and_scope_form.html',
             'project_role_form': 'formtools/wizard/project_role_form.html',}


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
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        return self.model.objects.get_project(self.request.user.id).distinct()









