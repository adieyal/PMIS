from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='main.html'), name='main'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace='accounts')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^account/', include('project.apps.account.urls', namespace='account')),
    url(r'^reports/', include('project.apps.reports.urls', namespace='reports')),
    url(r'^entry/', include('project.apps.entry.urls', namespace='entry')),
    url(r'^ui/', include('project.apps.ui.urls', namespace='ui')),
    url(r'^v2/', include('project.apps.v2.urls', namespace='v2')),
)
