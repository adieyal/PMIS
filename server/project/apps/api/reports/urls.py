from django.conf.urls import patterns, url, include
import district_report

urlpatterns = patterns('project.apps.api.reports.district_report',
    url(r'^district/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'district_report', name='reports_district'),
    url(r'^district/(?P<district_id>\d+)/dashboard/(?P<year>\d+)/(?P<month>\d+)/graphs/$', 'dashboard_graphs', name='reports_district_graphs'),
)

