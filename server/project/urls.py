from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='main.html'), name='main'),
    url(r'^api/', include('project.apps.api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^projects/', include('project.apps.projects.urls', namespace='projects')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),

    #url(r'^reports2/district/dashboard/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', TemplateView.as_view(template_name='reports/district/index.html'), name='district_dashboard'),
    #url(r'^reports2/district/progress/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', TemplateView.as_view(template_name='reports/district/progress.html'), name='district_progress'),
    #url(r'^reports2/district/perform/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', TemplateView.as_view(template_name='reports/district/perform.html'), name='district_perform'),

    url(r'^reports/district/dashboard/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'project.apps.reports.views.district_dashboard', name='district_dashboard_report'),
    url(r'^reports/district/progress/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'project.apps.reports.views.district_progress', name='district_progress_report'),
    url(r'^reports/district/perform/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', 'project.apps.reports.views.district_perform', name='district_perform_report'),
)
