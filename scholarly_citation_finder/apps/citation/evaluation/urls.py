from django.conf.urls import url

import views


urlpatterns = [
    url(r'^create/(?P<name>[a-z]+)$', views.create),
    url(r'^create/(?P<id>[0-9]+)/$', views.create_detail),
    url(r'^run/(?P<name>[a-z]+)/$', views.run),
]
