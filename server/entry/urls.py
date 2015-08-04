from django.conf.urls import patterns, url, include

urlpatterns = patterns('entry.views',
    url(r'^(?P<project_id>[\w-]+)/edit$', 'edit', {}, 'edit'),
    url(r'^new$', 'new', {}, 'new'),
    url(r'^$', 'projects', {}, 'list'),
    url(r'^diagnose$', 'diagnose', {}, 'diagnose'),
    url(r'^cluster$', 'cluster', {}, 'cluster'),
    url(r'^coordinator$', 'coordinator', {}, 'coordinator'),
    url(r'^contractor$', 'contractor', {}, 'contractor'),
    url(r'^programme$', 'programme', {}, 'programme'),
    url(r'^projects$', 'projects_json', {}, 'projects'),
)
