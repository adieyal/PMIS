from django.contrib import admin
from models import Cluster, Programme, ImplementingAgent


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Cluster, ClusterAdmin)

class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cluster')
    list_filter = ('cluster',)
admin.site.register(Programme, ProgrammeAdmin)

class ImplementingAgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(ImplementingAgent, ImplementingAgentAdmin)

