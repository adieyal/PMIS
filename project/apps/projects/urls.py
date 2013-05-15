from django.conf.urls import patterns, include, url
from project.apps.projects.views import ProjectView

urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='project_view'),



                       )
