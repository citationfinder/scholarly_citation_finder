"""scholarly_citation_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from rest_framework import routers

from .apps.core.admin import default_site, mag_site
from scholarly_citation_finder.apps.rest import views

router = routers.DefaultRouter()
router.register(r'affiliation', views.AffiliationViewSet)
router.register(r'conference', views.ConferenceViewSet)
router.register(r'conferenceinstance', views.ConferenceInstanceViewSet)
router.register(r'fieldofstudy', views.FieldOfStudyViewSet)
router.register(r'journal', views.JournalViewSet)


urlpatterns = [
    # admin
    url(r'^admin/default/', include(default_site.urls)),
    url(r'^admin/mag/', include(mag_site.urls)),
    # rest
    url(r'^rest/', include('scholarly_citation_finder.apps.rest.urls')),
    # api
    url(r'^api/', include('scholarly_citation_finder.api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
