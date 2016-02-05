from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework.authtoken import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='main.html'), name='main'),
    url(r'^authtoken$', views.obtain_auth_token),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace='accounts')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^entry/', include('entry.urls', namespace='entry')),
)
