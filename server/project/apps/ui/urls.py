from django.conf.urls import patterns, url, include
from django.contrib.staticfiles import views

def ui_serve(request, path):
    return views.serve(request, '/ui/'+path)
    
urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', ui_serve),
)
