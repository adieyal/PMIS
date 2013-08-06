from django.conf.urls import patterns, url, include

urlpatterns = patterns('project.apps.reports.views',
    url(r'^district/(?P<district_id>\d+)/dashboard/(?P<year>\d+)/(?P<month>\d+)/$', 'district_dashboard', name='district_dashboard'),
    url(r'^district/(?P<district_id>\d+)/progress/(?P<year>\d+)/(?P<month>\d+)/$', 'district_progress', name='district_progress'),
    url(r'^district/(?P<district_id>\d+)/perform/(?P<year>\d+)/(?P<month>\d+)/$', 'district_perform', name='district_perform'),
)
