from django import forms
from project.apps.projects.models import Project, ProjectRole, Budget, Planning, ProjectMilestone, ScopeOfWork, ProjectFinancial


class UpdateModelForm(forms.ModelForm):
    id = forms.IntegerField(required=False)

    def clean_id(self):
        id_ = self.cleaned_data['id']
        if id_:
            if self._meta.model.objects.filter(id=id_).exists():
                self.instance = self._meta.model.objects.get(id=id_)
            else:
                self.instance = self._meta.model()
        else:
            self.instance = self._meta.model()
        return id_


class ProjectTestForm(UpdateModelForm):

    class Meta:
        model = Project


class ProjectRoleTestForm(UpdateModelForm):

    class Meta:
        model = ProjectRole


class BudgetTestForm(UpdateModelForm):

    class Meta:
        model = Budget


class PlanningTestForm(UpdateModelForm):

    class Meta:
        model = Planning


class ProjectMilestoneTestForm(UpdateModelForm):

    class Meta:
        model = ProjectMilestone


class ScopeOfWorkTestForm(UpdateModelForm):

    class Meta:
        model = ScopeOfWork


class ProjectFinancialTestForm(UpdateModelForm):

    class Meta:
        model = ProjectFinancial