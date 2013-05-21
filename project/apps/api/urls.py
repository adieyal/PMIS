from django.conf.urls import patterns, url, include
import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^clients/$', views.ClientViewSet.as_view({'get': 'list'}), name='clients_view'),
                       url(r'^districts/$', views.DistrictViewSet.as_view({'get': 'list'}), name='districts_view'),
                       url(r'^districts/(?P<pk>\d+)/municipalities/$', views.MunicipalityViewSet.as_view({'get': 'retrieve'}), name='municipalities_view'),
                       url(r'^clients/(?P<pk>\d+)/programmes/$', views.ProgrammeViewSet.as_view({'get': 'retrieve'}), name='programmes_view'),
                       url(r'^clients/(?P<pk>\d+)/projects/$', views.ProjectViewSet.as_view({'get': 'retrieve'}), name='project_view'),
                       url(r'^districts/(?P<pk>\d+)/projects/$', views.ProjectInDistrictViewSet.as_view({'get': 'retrieve'})),
                       url(r'^municipalities/(?P<pk>\d+)/projects/$', views.ProjectInMunicipalityViewSet.as_view({'get': 'retrieve'})),
                       url(r'^programmes/(?P<pk>\d+)/projects/$', views.ProjectInProgrammeViewSet.as_view({'get': 'retrieve'})),
                       url(r'^projects/(?P<pk>\d+)/progress/$', views.ProgressView.as_view({'get': 'retrieve'})),
                       url(r'^projects/(?P<pk>\d+)/comments/$', views.ProjectCommentsViewSet.as_view({'get': 'retrieve'})),
)