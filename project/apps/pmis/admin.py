from django.contrib import admin
from revisions.admin import VersionedAdmin
from models import Client, Programme, Project, Municipality, District, ProjectPeople, PeopleType


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class ProgrammeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'client')


class ProjectAdmin(VersionedAdmin):
    fields = ('name', 'description', 'programme', 'municipality', 'district', 'update_date', 'update_comment', 'update_user')


class MunicipalityAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


class DistrictAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'municipality')


class ProjectPeopleAdmin(admin.ModelAdmin):
    fields = ('name', 'project', 'people_type')


class PeopleTypeAdmin(admin.ModelAdmin):
    fields = ('name',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ProjectPeople, ProjectPeopleAdmin)
admin.site.register(PeopleType, PeopleTypeAdmin)
