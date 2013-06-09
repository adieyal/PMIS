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
            meta=((model.Versioned, {"update_comment": update_comment, "update_user_id": update_user_id}),),
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
            meta=((model.Versioned, {"update_comment": update_comment, "update_user_id": update_user_id}),),
            db = self.revision_context_manager.get_db(),
        )


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')


class ProjectAdmin(CustomVersionAdmin):
    form = ProjectVersionedForm


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
    fields = ('month', 'year', 'planned_expenses', 'planned_progress', 'project')


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
    list_filter = ('milestone',) 


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('phase', 'name', 'order')


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
admin.site.register(model.ProjectRole, ProjectRoleAdmin)
admin.site.register(model.Planning, PlanningAdmin)
admin.site.register(model.MonthlySubmission, MonthlySubmissionAdmin)
admin.site.register(model.CommentType, CommentTypeAdmin)
admin.site.register(model.ProjectStatus, ProjectStatusAdmin)
admin.site.register(model.VarianceOrder, VarianceOrderAdmin)
admin.site.register(model.Milestone, MilestoneAdmin)
admin.site.register(model.ProjectFinancial, ProjectFinancialAdmin)
admin.site.register(model.ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(model.Budget)
admin.site.register(model.GroupPerm, GroupPermAdmin)
admin.site.register(model.GroupPermObj)
admin.site.register(model.Versioned, VersionedAdmin)
admin.site.register(model.ScopeCode)
