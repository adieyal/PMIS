from django import forms
from django.contrib.auth.models import User
from .models import Project, MonthlySubmission, ProjectStatus, VarianceOrder, ProjectMilestone, ProjectFinancial


class VersionedForm(forms.ModelForm):
    # custom field not backed by database
    update_comment = forms.CharField(widget=forms.Textarea())
    update_user = forms.ChoiceField(choices=User.objects.all().values_list('id', 'username'))


class ProjectVersionedForm(VersionedForm):

    class Meta:
        model = Project
        fields = ('name', 'programme', 'description', 'municipality',)


class MonthlySubmissionVersionedForm(VersionedForm):
    class Meta:
        model = MonthlySubmission
        fieldsets = (
            ('Date', {'fields': ('month', 'year')}),
            ('Project', {'fields': ('project',)}),
            (None, {'fields': ('actual_expenditure', 'actual_progress')}),
            ('Comment', {'fields': ('comment', 'comment_type', 'remedial_action')}),
        )


class ProjectStatusVersionedForm(VersionedForm):
    class Meta:
        model = ProjectStatus
        fieldsets = (
            (None, {'fields': ('project', 'status')}),
        )


class VarianceOrderVersionedForm(VersionedForm):
    class Meta:
        model = VarianceOrder
        fieldsets = (
            (None, {'fields': ('project', 'description', 'amount')}),
        )


class ProjectMilestoneVersionedForm(VersionedForm):
    class Meta:
        model = ProjectMilestone
        fieldsets = (
            (None, {'fields': ('project', 'completion_date')}),
        )


class ProjectFinancialVersionedForm(VersionedForm):
    class Meta:
        model = ProjectFinancial
        fieldsets = (
            (None, {'fields': ('total_anticipated_cost', 'project_planning_budget', 'project')}),
        )