from django.conf.urls import url

import views


urlpatterns = [
    url(r'^evaluation/create/$', views.evaluation_create),
    url(r'^evaluation/job/(?P<name>.*)/status/$', views.evaluation_status),
    url(r'^evaluation/job/(?P<name>.*)/authors/$', views.evaluation_authors),
]
