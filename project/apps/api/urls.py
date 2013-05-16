from django.conf.urls import patterns, url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'districts', views.DistrictViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^districts/(?P<pk>\d+)/municipalities/', views.MunicipalityViewSet.as_view({'get': 'retrieve'})),
                       url(r'^clients/(?P<pk>\d+)/programmes/', views.ProgrammeViewSet.as_view({'get': 'retrieve'})),
                       url(r'^clients/(?P<pk>\d+)/projects/', views.ProjectViewSet.as_view({'get': 'retrieve'})),
                       # url(r'^districts/(?P<pk>\d+)/projects/', views.ProjectViewSet.as_view()),
)