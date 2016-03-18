from django.conf.urls import include, url
from rest_framework import routers

from scholarly_citation_finder.apps.rest import views
from scholarly_citation_finder.tools.harvester.models import HarvesterViewSet
from scholarly_citation_finder.apps.tasks.models import TaskViewSet


default_router = routers.DefaultRouter()
default_router.register(r'harvester', HarvesterViewSet)
default_router.register(r'tasks', TaskViewSet)


mag_router = routers.DefaultRouter()
mag_router.register(r'publication', views.PublicationViewSet)


urlpatterns = [
    url(r'^default/', include(default_router.urls)),
    url(r'^mag/', include(mag_router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
