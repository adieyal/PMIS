from django.conf.urls import patterns, url, include
from django.contrib.staticfiles import views

def v2_serve(request, path):
    return views.serve(request, '/v2/' + path)
    
urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', v2_serve),
)
