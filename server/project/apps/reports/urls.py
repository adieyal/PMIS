from django.conf.urls import patterns, url, include

urlpatterns = patterns('project.apps.reports.views',
    url(r'^test/$', 'test'),
    url(r'^district/(?P<district_id>\d+)/dashboard/(?P<year>\d+)/(?P<month>\d+)/$', 'district_dashboard', name='district_dashboard'),
    url(r'^district/(?P<district_id>\d+)/progress/(?P<year>\d+)/(?P<month>\d+)/$', 'district_progress', name='district_progress'),
    url(r'^district/(?P<district_id>\d+)/perform/(?P<year>\d+)/(?P<month>\d+)/$', 'district_perform', name='district_perform'),
    
    url(r'^(?P<report>\w+)/(?P<report_id>\w+)/(?P<subreport>\w+)/(?P<year>\d{d})/(?P<month>\d{2})/$',
        'generic_report', name='generic_report'),
    url(r'^(?P<report>\w+)/(?P<subreport>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        'generic_report', { 'report_id': None }, name='generic_report'),
    url(r'^(?P<report>\w+)/(?P<report_id>\w+)/(?P<subreport>\w+)/(?P<year>\d{d})/(?P<month>\d{2})/json$',
        'generic_json', name='generic_report_json'),
    url(r'^(?P<report>\w+)/(?P<subreport>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/json$',
        'generic_json', { 'report_id': None }, name='generic_report_json'),
)
