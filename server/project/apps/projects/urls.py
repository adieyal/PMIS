from django.conf.urls import patterns, include, url
from project.apps.projects.forms import ProjectForm, LocationForm, LocationAndScopeFormContainer, ProjectRoleFormSet
from project.apps.projects.views import ProjectView, CreateProjectWizard, FORMS, ProjectListView

urlpatterns = patterns('',
                       url(r'^$', ProjectListView.as_view(), name='project_list_view'),
                       url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='project_view'),
                       url(r'^create_project/$', CreateProjectWizard.as_view(FORMS), name='create_project'),



                       )
