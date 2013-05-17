from django.contrib import admin
import reversion
from revisions.admin import VersionedAdmin
from models import Client, Programme, Project, Municipality, District, Entity, Role, ProjectRole, Planning, MonthlySubmission, CommentType, ProjectStatus, VarianceOrder, Milestone, ProjectFinancial, Versioned
from project.apps.projects.forms import ProjectVersionedForm, MonthlySubmissionVersionedForm, ProjectStatusVersionedForm, VarianceOrderVersionedForm, ProjectMilestoneVersionedForm, ProjectFinancialVersionedForm


class CustomVersionAdmin(reversion.VersionAdmin):
    def log_change(self, request, object, message):
        super(reversion.VersionAdmin, self).log_change(request, object, message)
        update_comment = request.POST['update_comment']
        update_user_id = request.POST['update_user']
        self.revision_manager.save_revision(
            self.get_revision_data(request, object, reversion.models.VERSION_CHANGE),
            user=request.user,
            comment=message,
            ignore_duplicates=self.ignore_duplicate_revisions,
            meta=((Versioned, {"update_comment": update_comment, "update_user_id": update_user_id}),),
            db = self.revision_context_manager.get_db(),
            )


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')


class ProjectAdmin(CustomVersionAdmin):
    form = ProjectVersionedForm


class MunicipalityAdmin(admin.TabularInline):
    model = Municipality


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


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('phase', 'name', 'order')


class ProjectFinancialAdmin(CustomVersionAdmin):
    form = ProjectFinancialVersionedForm


admin.site.register(Client, ClientAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Project, ProjectAdmin)

admin.site.register(District, DistrictAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
admin.site.register(Planning, PlanningAdmin)
admin.site.register(MonthlySubmission, MonthlySubmissionAdmin)
admin.site.register(CommentType, CommentTypeAdmin)
admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(VarianceOrder, VarianceOrderAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(ProjectFinancial, ProjectFinancialAdmin)
