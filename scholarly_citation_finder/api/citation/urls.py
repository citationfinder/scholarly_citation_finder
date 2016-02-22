from django.conf.urls import url

import views


urlpatterns = [
    url(r'^evaluation/(?P<name>.*)/status/$', views.evaluation_status),
    url(r'^evaluation/(?P<name>.*)/authors/$', views.evaluation_authors),
    #url(r'^$', views.index, name='index'),
]
