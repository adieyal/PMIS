from django.contrib import admin
from revisions.admin import VersionedAdmin
from models import Client, Programme, Project, Municipality, District, Entity, Role, ProjectRole, Planning, MonthlySubmission, CommentType, ProjectStatus, VarianceOrder, Milestone


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')


class ProjectAdmin(VersionedAdmin):
    fields = (
        'name', 'programme', 'municipality', 'district', 'update_date', 'update_comment', 'update_user')


class MunicipalityAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'district')


class DistrictAdmin(admin.ModelAdmin):
    fields = ('name', 'description',)


class EntityAdmin(admin.ModelAdmin):
    fields = ('name', )


class RoleAdmin(admin.ModelAdmin):
    fields = ('name',)


class ProjectRoleAdmin(admin.ModelAdmin):
    fields = ('project', 'role', 'entity')


class PlanningAdmin(admin.ModelAdmin):
    fields = ('month', 'year', 'planned_expenses', 'planned_progress', 'project')


class MonthlySubmissionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Date', {'fields': ('month', 'year')}),
        ('Project', {'fields': ('project',)}),
        (None, {'fields': ('actual_expenditure', 'actual_progress')}),
        ('Comment', {'fields': ('comment', 'comment_type', 'remedial_action')}),
    )


class CommentTypeAdmin(admin.ModelAdmin):
    fields = ('name',)


class ProjectStatusAdmin(VersionedAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'status')}),
        ('Description versioned', {'fields': ('update_date', 'update_comment', 'update_user')}),
    )


class VarianceOrderAdmin(VersionedAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'description', 'amount')}),
        ('Description versioned', {'fields': ('update_date', 'update_comment', 'update_user')}),
    )


class ProjectMilestoneAdmin(VersionedAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'completion_date')}),
        ('Description versioned', {'fields': ('update_date', 'update_comment', 'update_user')}),
    )


class MilestoneAdmin(admin.ModelAdmin):
    fields = ('phase', 'name', 'order')

admin.site.register(Client, ClientAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
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
