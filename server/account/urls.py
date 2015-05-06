from django.conf.urls import patterns, url, include

urlpatterns = patterns('account.views',
    url(r'^login$', 'login', {}, 'logout'),
    url(r'^logout$', 'logout', {}, 'login'),
    url(r'^session$', 'session', {}, 'session'),
)
