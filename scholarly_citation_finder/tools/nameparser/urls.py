from django.conf.urls import url

import views


urlpatterns = [
    url(r'^humanname/$', views.humanname),
    url(r'^stringmatching/$', views.stringmatching),
]
