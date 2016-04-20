from django.conf.urls import include, url

import views


urlpatterns = [
    url(r'^mag/', include('scholarly_citation_finder.apps.citation.mag.urls')),
    url(r'^evaluation/', include('scholarly_citation_finder.apps.citation.evaluation.urls')),
    url(r'^citations/find/$', views.citations_find),
    url(r'^citations/cron/$', views.citations_cron),
]
