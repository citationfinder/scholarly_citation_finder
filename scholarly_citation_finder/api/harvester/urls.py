from django.conf.urls import url

import views


urlpatterns = [
    url(r'^oaipmh/(?P<name>[a-z]+)/', views.oaipmh),
]
