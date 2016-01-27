from django.conf.urls import include, url
from rest_framework import routers

from scholarly_citation_finder.apps.core.admin import default_site, mag_site
from scholarly_citation_finder.apps.rest import views


router = routers.DefaultRouter()
router.register(r'affiliation', views.AffiliationViewSet)
router.register(r'conference', views.ConferenceViewSet)
router.register(r'conferenceinstance', views.ConferenceInstanceViewSet)
router.register(r'fieldofstudy', views.FieldOfStudyViewSet)
router.register(r'journal', views.JournalViewSet)


urlpatterns = [
    url(r'^mag/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
