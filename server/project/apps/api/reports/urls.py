from django.conf.urls import patterns, url, include
import district_report
import headoffice_report

urlpatterns = patterns('project.apps.api.reports',
    url(r'^district/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'district_report.district_report', name='district'),
    url(r'^district/(?P<district_id>\d+)/dashboard/(?P<year>\d+)/(?P<month>\d+)/graphs/$', 'district_report.dashboard_graphs', name='district_graphs'),
    url(r'^headoffice/dashboard/(?P<year>\d+)/(?P<month>\d+)/$', 'headoffice_report.headoffice_dashboard', name='headoffice_dashboard'),
)

