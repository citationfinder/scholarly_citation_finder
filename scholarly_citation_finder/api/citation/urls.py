from django.conf.urls import url

import views


urlpatterns = [
    url(r'^mag/authors-citations/(?P<id>[0-9]+)/$', views.mag_authors_citations_result),
    url(r'^mag/authors-citations/$', views.mag_authors_citations),
    #url(r'^evaluation/create/$', views.evaluation_create),
    url(r'^evaluation/job/(?P<name>.*)/status/$', views.evaluation_status),
    url(r'^evaluation/job/(?P<name>.*)/authors/$', views.evaluation_authors),
]
