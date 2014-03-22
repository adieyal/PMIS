from django.conf.urls import patterns, url, include

urlpatterns = patterns('project.apps.entry.views',
    url(r'^(?P<project_id>[\w-]+)/edit$', 'project', {}, 'project'),
    url(r'^$', 'list', {}, 'list'),
)
