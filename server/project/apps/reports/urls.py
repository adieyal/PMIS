from django.conf.urls import patterns, url, include

urlpatterns = patterns('project.apps.reports.views',
    url(r'^test/$', 'test'),
    url(r'^district/dashboard/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'district_dashboard', name='district_dashboard'),
    url(r'^district/progress/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'district_progress', name='district_progress'),
    url(r'^district/perform/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'district_perform', name='district_perform'),

    url(r'^cluster/(?P<subreport>\w+)/(?P<client_code>[a-z]+)/(?P<year>\d+)/(?P<month>\d+)/$', 'cluster_report', name='cluster_report'),

    url(r'^cluster/(?P<subreport>\w+)/(?P<client_code>[a-z]+)/(?P<year>\d+)/(?P<month>\d+)/json$', 'generic_json', {'report': 'cluster'}, name='cluster_report_json'),

    url(r'^project/(?P<project_id>[\w-]+)/project/(?P<year>\d{4})/(?P<month>\d{2})/json$',
        'project_json', {}, name='project_report_json'),

    url(r'^project/(?P<project_id>[\w-]+)/json$',
        'project_json', {}, name='project_json'),

    url(r'^(?P<report>\w+)/(?P<report_id>[\w-]+)/(?P<subreport>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        'generic_report', name='generic_report'),
    url(r'^(?P<report>\w+)/(?P<subreport>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        'generic_report', { 'report_id': None }, name='generic_report'),
    url(r'^(?P<report>\w+)/(?P<report_id>\w+)/(?P<subreport>\w+)/(?P<year>\d{d})/(?P<month>\d{2})/json$',
        'generic_json', name='generic_report_json'),
    url(r'^(?P<report>\w+)/(?P<subreport>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/json$',
        'generic_json', { 'report_id': None }, name='generic_report_json'),
             
    url(r'^project/$', 'project_list', {}, name='project_list'),          
                       
)
