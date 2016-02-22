from django.conf.urls import url

import views


urlpatterns = [
    url(r'^evaluation/(?P<name>[a-z0-1]+)/status/$', views.evaluation_status),
    url(r'^evaluation/(?P<name>[a-z0-1]+)/authors/$', views.evaluation_authors),
    #url(r'^$', views.index, name='index'),
]
