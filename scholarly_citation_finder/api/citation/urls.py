from django.conf.urls import include, url

import views


urlpatterns = [
    url(r'^mag/', include('scholarly_citation_finder.api.citation.mag.urls')),
    url(r'^evaluation/create/(?P<id>[0-9]+)/$', views.evaluation_detail),
    url(r'^evaluation/create/(?P<name>[a-z]+)$', views.evaluation_create),
    url(r'^evaluation/run/(?P<name>[a-z]+)/$', views.evaluation_run),
    url(r'^evaluation/find/$', views.evaluation_find),
]
