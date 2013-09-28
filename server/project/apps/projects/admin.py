from django.contrib import admin
import reversion
import models
from project.apps.projects.forms import ProjectVersionedForm, MonthlySubmissionVersionedForm, ProjectStatusVersionedForm, VarianceOrderVersionedForm, ProjectMilestoneVersionedForm, ProjectFinancialVersionedForm


class CustomVersionAdmin(reversion.VersionAdmin):
    def log_addition(self, request, object):
        update_comment = request.POST['update_comment']
        update_user_id = request.POST['update_user']
        self.revision_manager.save_revision(
            self.get_revision_data(request, object, reversion.models.VERSION_ADD),
            user=request.user,
            comment="Initial version.",
            ignore_duplicates=self.ignore_duplicate_revisions,
            meta=((models.Versioned, {"update_comment": update_comment, "update_user_id": update_user_id}),),
            db=self.revision_context_manager.get_db(),
        )

    def log_change(self, request, object, message):
        update_comment = request.POST['update_comment']
        update_user_id = request.POST['update_user']
        self.revision_manager.save_revision(
            self.get_revision_data(request, object, reversion.models.VERSION_CHANGE),
            user=request.user,
            comment=message,
            ignore_duplicates=self.ignore_duplicate_revisions,
            meta=((models.Versioned, {"update_comment": update_comment, "update_user_id": update_user_id}),),
            db = self.revision_context_manager.get_db(),
        )


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')
    list_display = ('name', 'client')
    list_filter = ('client',)
    



class ProjectFinancialInlineAdmin(admin.TabularInline):
    model = models.ProjectFinancial


class BudgetInlineAdmin(admin.TabularInline):
    model = models.Budget
    extra = 0


class PlanningInlineAdmin(admin.TabularInline):
    model = models.Planning
    extra = 0


class ProjectMilestoneInlineAdmin(admin.TabularInline):
    model = models.ProjectMilestone
    extra = 0


class ProjectRoleInlineAdmin(admin.TabularInline):
    model = models.ProjectRole


class ScopeOfWorkInlineAdmin(admin.TabularInline):
    model = models.ScopeOfWork
    extra = 0


class MonthlySubmissionInlineAdmin(admin.TabularInline):
    model = models.MonthlySubmission
    extra = 0


class ProjectAdmin(CustomVersionAdmin):
    form = ProjectVersionedForm
    list_display = ('name', 'municipality', 'district', 'programme', 'current_step')
    list_filter = ("programme", "municipality__district", "current_step", "current_step__phase", "programme__client")
    inlines = (ScopeOfWorkInlineAdmin, ProjectFinancialInlineAdmin, BudgetInlineAdmin, PlanningInlineAdmin, ProjectMilestoneInlineAdmin, ProjectRoleInlineAdmin, MonthlySubmissionInlineAdmin)

    @property
    def district(self, instance):
        return instance.municipality.district


class MunicipalityAdmin(admin.TabularInline):
    model = models.Municipality


class DistrictAdmin(admin.ModelAdmin):
    inlines = [MunicipalityAdmin, ]


class EntityAdmin(admin.ModelAdmin):
    fields = ('name', )


class RoleAdmin(admin.ModelAdmin):
    fields = ('name',)

class ProjectRoleAdmin(admin.ModelAdmin):
    fields = ('project', 'role', 'entity')


class PlanningAdmin(admin.ModelAdmin):
    fields = ('date', 'planned_expenses', 'planned_progress', 'project')


class MonthlySubmissionAdmin(CustomVersionAdmin):
    form = MonthlySubmissionVersionedForm


class CommentTypeAdmin(admin.ModelAdmin):
    fields = ('name',)


class ProjectStatusAdmin(CustomVersionAdmin):
    form = ProjectStatusVersionedForm


class VarianceOrderAdmin(CustomVersionAdmin):
    form = VarianceOrderVersionedForm


class ProjectMilestoneAdmin(CustomVersionAdmin):
    form = ProjectMilestoneVersionedForm
    list_filter = ('project', 'milestone',)
    list_display = ('project', 'milestone', 'completion_date')


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('phase', 'name', 'order')
    list_filter = ('phase',)


class ProjectFinancialAdmin(CustomVersionAdmin):
    form = ProjectFinancialVersionedForm


class GroupPermAdmin(admin.ModelAdmin):
    fields = ('user',)
    filter_horizontal = ('user',)


class VersionedAdmin(admin.ModelAdmin):
    fields = ('update_comment', 'update_user')


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Programme, ProgrammeAdmin)
admin.site.register(models.Project, ProjectAdmin)

admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Entity, EntityAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.ProjectRole, ProjectRoleAdmin)
admin.site.register(models.Planning, PlanningAdmin)
admin.site.register(models.MonthlySubmission, MonthlySubmissionAdmin)
admin.site.register(models.CommentType, CommentTypeAdmin)
admin.site.register(models.ProjectStatus, ProjectStatusAdmin)
admin.site.register(models.VarianceOrder, VarianceOrderAdmin)
admin.site.register(models.Milestone, MilestoneAdmin)
admin.site.register(models.ProjectFinancial, ProjectFinancialAdmin)
admin.site.register(models.ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(models.Budget)
admin.site.register(models.GroupPerm, GroupPermAdmin)
admin.site.register(models.GroupPermObj)
admin.site.register(models.Versioned, VersionedAdmin)
admin.site.register(models.ScopeCode)
admin.site.register(models.ScopeOfWork)
