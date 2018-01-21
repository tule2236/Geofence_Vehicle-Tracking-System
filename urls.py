from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from geofence.views import VehicleSearchListView, VehicleList
from geofence.models import Vehicle 
from django.views.generic import ListView

urlpatterns = [url(r'^APSG_geofence', views.APSG_geofence), 
				url(r'^TMSG_geofence', views.TMSG_geofence), 
				url(r'^geolist$', VehicleList.as_view()) ,
				url(r'^update_driver/(?P<pk>\d+)/$', views.update_driver_db,  name = 'update_driver_db'),
				url(r'^update_geofence/(?P<pk>\d+)/$', views.geofence_assignment,  name = 'geofence_assignment'),
				url(r'^update_child_geofence/(?P<pk>\d+)/$', views.child_geofence_assignment,  name = 'child_geofence_assignment'),
				url(r'^vehicle_search$', VehicleSearchListView.as_view(), name = 'post'),
				url(r'^geofence_assigned$', VehicleSearchListView.as_view(), name = 'post'),
				]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
				# url(r'^geofence/', views.update_driver_db, name = 'update_driver_db')]
				# url(r'^geofence', views.geofence,  name = 'geofence') ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

