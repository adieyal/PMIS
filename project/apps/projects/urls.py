from django.conf.urls import patterns, include, url
from project.apps.projects.forms import ProjectForm, LocationAndScopeForm, LocationAndScopeFormSet
from project.apps.projects.views import ProjectView, CreateProjectWizard

urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='project_view'),
                       url(r'^create_project/$', CreateProjectWizard.as_view([ProjectForm, LocationAndScopeFormSet, ])),



                       )
