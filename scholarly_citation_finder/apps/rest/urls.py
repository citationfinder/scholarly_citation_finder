from django.conf.urls import include, url
from rest_framework import routers

from scholarly_citation_finder.apps.rest import views


router = routers.DefaultRouter()
router.register(r'publication', views.PublicationViewSet)


urlpatterns = [
    url(r'^mag/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
