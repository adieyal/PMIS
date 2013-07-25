from django.conf.urls import patterns, url, include
import district_report

urlpatterns = patterns('',
    url(r'^reports/district/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', district_report.district_report, name='reports_district'),
)

