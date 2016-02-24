from django.conf.urls import include, url

import views


urlpatterns = [
    url(r'^mag/', include('scholarly_citation_finder.api.citation.mag.urls')),
    url(r'^evaluation/job/(?P<name>.*)/status/$', views.evaluation_status),
    url(r'^evaluation/job/(?P<name>.*)/authors/$', views.evaluation_authors),
]
