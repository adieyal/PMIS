from django.conf.urls import patterns, url, include
import views
import reports


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
   url(r'^clients/$', views.ClientViewSet.as_view(), name='clients_view'),
   url(r'^districts/$', views.DistrictViewSet.as_view({'get': 'list'}), name='districts_view'),
   url(r'^projects/$', views.ProjectsView.as_view(), name='projects_view'),
   url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_detail_view'),
   url(r'^programmes/$', views.ProgrammeViewSet.as_view(), name='programme_view'),
   url(r'^scope_codes/$', views.ScopeCodeViewSet.as_view(), name='scope_codes_view'),
   url(r'^roles/$', views.RolesViewSet.as_view(), name='roles_view'),
   url(r'^entities/$', views.EntitiesViewSet.as_view(), name='entities_view'),
   url(r'^milestones/$', views.MilestonesViewSet.as_view(), name='milestones_view'),
   url(r'^districts/(?P<pk>\d+)/municipalities/$', views.MunicipalityViewSet.as_view(), name='municipalities_view'),
   url(r'^clients/(?P<pk>\d+)/programmes/$', views.ProgrammeOfClientViewSet.as_view(), name='programmes_of_client_view'),
   url(r'^clients/(?P<pk>\d+)/projects/$', views.ProjectOfClientViewSet.as_view({'get': 'retrieve'}), name='project_of_client_view'),
   url(r'^clients/(?P<client_id>\d+)/districts/(?P<district_id>\d+)/projects/$', views.ProjectOfClientOfDistrictViewSet.as_view(), name='project_of_client_of_district_view'),

   url(r'^districts/(?P<pk>\d+)/projects/$', views.ProjectInDistrictViewSet.as_view({'get': 'retrieve'}), name='project_in_district_view'),
   url(r'^municipalities/(?P<pk>\d+)/projects/$', views.ProjectInMunicipalityViewSet.as_view({'get': 'retrieve'}), name='project_in_municipality_view'),
   url(r'^programmes/(?P<pk>\d+)/projects/$', views.ProjectInProgrammeViewSet.as_view({'get': 'retrieve'}), name='project_in_programme_view'),
   url(r'^projects/(?P<pk>\d+)/progress/$', views.ProgressView.as_view(), name='progress_view'),
   url(r'^projects/(?P<pk>\d+)/comments/$', views.ProjectCommentsViewSet.as_view({'get': 'retrieve'}), name='project_comments_view'),
   url(r'^clients/(?P<client_id>\d+)/districts/(?P<district_id>\d+)/projects/top_performing/$', views.ProjectTopPerformingViewSet.as_view(), name='project_top_performing_view'),
   url(r'^clients/(?P<client_id>\d+)/districts/(?P<district_id>\d+)/projects/worst_performing/$', views.ProjectWorstPerformingViewSet.as_view(), name='project_worst_performing_view'),
   url(r'^clients/(?P<client_id>\d+)/districts/(?P<district_id>\d+)/projects/implementation/overall_progress/$', views.ProjectOverallProgressViewSet.as_view(), name='project_overall_progress_view'),
)

# Add report apis
urlpatterns += patterns('',
    url(r'^reports/district/(?P<district_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', reports.district_report, name='reports_district'),
)
