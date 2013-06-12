from django.conf.urls import patterns, url, include
import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
   url(r'^clients/$', views.ClientViewSet.as_view(), name='clients_view'),
   url(r'^districts/$', views.DistrictViewSet.as_view({'get': 'list'}), name='districts_view'),
   url(r'^projects/$', views.ProjectViewSet.as_view(), name='project_view'),
   url(r'^programmes/$', views.ProgrammeViewSet.as_view(), name='programme_view'),
   url(r'^scope_codes/$', views.ScopeCodeViewSet.as_view(), name='scope_codes_view'),
   url(r'^roles/$', views.RolesViewSet.as_view(), name='roles_view'),
   url(r'^entities/$', views.EntitiesViewSet.as_view(), name='entities_view'),
   url(r'^milestones/$', views.MilestonesViewSet.as_view(), name='milestones_view'),
   url(r'^districts/(?P<pk>\d+)/municipalities/$', views.MunicipalityViewSet.as_view(), name='municipalities_view'),
   url(r'^clients/(?P<pk>\d+)/programmes/$', views.ProgrammeOfClientViewSet.as_view({'get': 'retrieve'}), name='programmes_of_client_view'),
   url(r'^clients/(?P<pk>\d+)/projects/$', views.ProjectOfClientViewSet.as_view({'get': 'retrieve'}), name='project_of_client_view'),
   url(r'^districts/(?P<pk>\d+)/projects/$', views.ProjectInDistrictViewSet.as_view({'get': 'retrieve'}), name='project_in_district_view'),
   url(r'^municipalities/(?P<pk>\d+)/projects/$', views.ProjectInMunicipalityViewSet.as_view({'get': 'retrieve'}), name='project_in_municipality_view'),
   url(r'^programmes/(?P<pk>\d+)/projects/$', views.ProjectInProgrammeViewSet.as_view({'get': 'retrieve'}), name='project_in_programme_view'),
   url(r'^projects/(?P<pk>\d+)/progress/$', views.ProgressView.as_view({'get': 'retrieve'}), name='progress_view'),
   url(r'^projects/(?P<pk>\d+)/comments/$', views.ProjectCommentsViewSet.as_view({'get': 'retrieve'}), name='project_comments_view'),
   url(r'^create_project/$', views.CreateProject.as_view(), name='create_project'),
   url(r'^update_project/$', views.UpdateProject.as_view(), name='update_project'),
   url(r'^project/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_detail_view'),
)
