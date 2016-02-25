from django.conf.urls import include, url
from rest_framework import routers

from scholarly_citation_finder.apps.rest import views
from scholarly_citation_finder.api.harvester.models import OaiPmhProviderViewSet


default_router = routers.DefaultRouter()
default_router.register(r'oaipmhprovider', OaiPmhProviderViewSet)


mag_router = routers.DefaultRouter()
mag_router.register(r'publication', views.PublicationViewSet)


urlpatterns = [
    url(r'^default/', include(default_router.urls)),               
    url(r'^mag/', include(mag_router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
