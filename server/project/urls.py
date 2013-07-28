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

    url(r'^reports/district/dashboard/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', TemplateView.as_view(template_name='reports/district/index.html'), name='district_dashboard'),
    url(r'^reports/district/progress/$', TemplateView.as_view(template_name='reports/district/progress.html'), name='district_progress'),
    url(r'^reports/district/perform/$', TemplateView.as_view(template_name='reports/district/perform.html'), name='district_perform'),

    # url(r'^', include(router.urls)),
)
