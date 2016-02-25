from django.conf.urls import include, url

import views


urlpatterns = [
    url(r'^mag/', include('scholarly_citation_finder.api.citation.mag.urls')),
    url(r'^evaluation/(?P<id>[0-9]+)/$', views.evaluation_detail),
    url(r'^evaluation/$', views.evaluation_index),
]
