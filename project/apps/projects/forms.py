from django import forms
# from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from .models import Project, MonthlySubmission, ProjectStatus, VarianceOrder, ProjectMilestone, ProjectFinancial, District, Municipality, ScopeOfWork


class VersionedForm(forms.ModelForm):
    # custom field not backed by database
    update_comment = forms.CharField(widget=forms.Textarea())
    update_user = forms.ChoiceField(choices=User.objects.all().values_list('id', 'username'))


class ProjectVersionedForm(VersionedForm):

    class Meta:
        model = Project
        fields = ('name', 'programme', 'project_number', 'description', 'municipality',)


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
            (None, {'fields': ('total_anticipated_cost', 'project')}),
        )


class ScopeOfWorkForm(forms.ModelForm):
    class Meta:
        model = ScopeOfWork
        fields = ['quantity', 'scope_code', ]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['programme', 'name', 'description', ]


class LocationAndScopeForm(forms.Form):
    # class Meta:
    #     model = Project
    district = forms.ChoiceField(choices=District.objects.all().values_list('id', 'name'))
    municipality = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Municipality.objects.all().values_list('id', 'name',))
    # scope = formset_factory(ScopeOfWorkForm)

LocationAndScopeFormSet = inlineformset_factory(Project, ScopeOfWork, form = LocationAndScopeForm, formset=ScopeOfWorkForm)
