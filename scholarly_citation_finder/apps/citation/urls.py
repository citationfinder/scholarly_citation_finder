from django.conf.urls import include, url

import views


urlpatterns = [
    url(r'^mag/', include('scholarly_citation_finder.apps.citation.mag.urls')),
    url(r'^evaluation/create/(?P<id>[0-9]+)/$', views.evaluation_detail),
    url(r'^evaluation/create/(?P<name>[a-z]+)$', views.evaluation_create),
    url(r'^evaluation/run/(?P<name>[a-z]+)/$', views.evaluation_run),
    url(r'^citations/find/$', views.citations_find),
    url(r'^citations/cron/$', views.citations_cron),
]
