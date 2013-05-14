from django.contrib import admin
from revisions.admin import VersionedAdmin
from models import Client, Programme, Project, Municipality, District, Entity, Role, ProjectRole, Planning, MonthlySubmission, CommentType, ProjectStatus


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')


class ProjectAdmin(VersionedAdmin):
    fields = (
        'name', 'description', 'programme', 'municipality', 'district', 'update_date', 'update_comment', 'update_user')


class MunicipalityAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class DistrictAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'municipality')


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
        (None, {'fields': ('actual_expenditure', 'actual_progress')}),
        ('Comment', {'fields': ('comment', 'comment_type', 'remedial_action')}),
    )


class CommentTypeAdmin(admin.ModelAdmin):
    fields = ('name',)


class ProjectStatusAdmin(VersionedAdmin):
    fields = ('project', 'status')


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
