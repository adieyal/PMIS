from django.conf.urls import patterns, url, include

urlpatterns = patterns('project.apps.entry.views',
    url(r'^(?P<project_id>[\w-]+)/edit$', 'edit', {}, 'edit'),
    url(r'^new$', 'new', {}, 'new'),
    url(r'^$', 'list', {}, 'list'),
    url(r'^coordinator$', 'coordinator', {}, 'coordinator'),
    url(r'^contractor$', 'contractor', {}, 'contractor'),
)
